# AGENTS.md

Conventions for AI agents and contributors working in this repository. These rules
apply to every pattern under `patterns/` and to the project as a whole.

> **Keep this file alive.** See [Keeping AGENTS.md up to date](#keeping-agentsmd-up-to-date)
> at the bottom. Whenever a new convention is introduced, agreed on in review, or
> applied to the codebase, update this file in the **same change** that introduces it.

---

## Project tooling

The project is managed with `uv`, with **all** configuration centralized in
`pyproject.toml`. Do not introduce parallel config files (`pytest.ini`,
`.coveragerc`, `setup.cfg`, `tox.ini`, etc.); fold any new setting into
`pyproject.toml` instead.

- **Python version**: `3.12` (pinned in `.python-version` and `requires-python`).
- **Dependency manager**: `uv` (lockfile `uv.lock` is committed; `.venv/` is local).
- **Task runner**: `poethepoet` via `[tool.poe.tasks]`. Never define ad-hoc shell
  scripts that duplicate a `poe` task; add or extend a task instead.
- **Formatter & linter**: `ruff` (replaces `black`). Configure under `[tool.ruff]`
  and `[tool.ruff.format]`.
- **Type checker**: `mypy` configured under `[tool.mypy]`.
- **Tests**: `pytest` + `pytest-cov`, all options under `[tool.pytest.ini_options]`
  and `[tool.coverage.*]`.

### Running things

Always invoke tools through `uv` so the right interpreter and lockfile are used:

```bash
uv run poe test          # fast test loop
uv run poe test-cov      # tests + coverage, fails under 100%
uv run poe format        # apply ruff formatting
uv run poe lint          # ruff lint
uv run poe check         # format --check + lint, used in CI
```

When adding a new pattern directory, scope `poe` tasks to it (don't broaden them
to the whole repo) and add it to `[tool.coverage.run].source`.

---

## Source-code conventions

### Determinism over mocks

When tests need stable output, make the **source** deterministic instead of
mocking in tests. Examples:

- Replace `uuid.uuid4()` with `uuid.uuid5(NAMESPACE, key)` and a fixed namespace
  (e.g. `uuid.UUID(int=5)`).
- Seed any randomness through an explicit parameter (`seed: int | None = None`)
  rather than relying on global state.

**Mocks are forbidden in tests.** If a test would need a mock, change the
production code so it doesn't.

### Type hints (Python 3.12)

- Prefer **built-in generics**: `list[X]`, `dict[K, V]`, `tuple[X, Y]`, `set[X]`.
- Prefer `collections.abc` over `typing` for abstract container types:
  `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Iterable`,
  `Iterator`, `Callable`.
- Use `X | None` instead of `Optional[X]`, and `A | B` instead of `Union[A, B]`.
- Reserve `typing` imports for things `collections.abc` doesn't cover
  (`Any`, `Protocol`, `TypeVar`, `cast`, etc.).

For dataclass fields, type the field by **what callers should see** and use a
matching factory:

```python
from collections.abc import MutableSequence
from dataclasses import dataclass, field

@dataclass
class CustomerSupport:
    tickets: MutableSequence[SupportTicket] = field(default_factory=list[SupportTicket])
```

### Type aliases

- Define type aliases **in the SUT**, never in tests.
- Re-export them from the package's `__init__.py` so tests can import them.
- **Do not create simple rename aliases** (e.g. `ProcessingStrategy = TicketOrderingStrategy`).
  If the original name is good enough, use it directly.

### Package layout & exports

Every variant directory is a real package and re-exports its public API from
`__init__.py`:

```python
# patterns/.../solution_05/__init__.py
from .main import main
from .support import (
    CustomerSupport,
    SupportTicket,
    TicketOrderingStrategy,
    fifo_strategy,
    filo_strategy,
    random_strategy,
)

__all__ = [
    "CustomerSupport",
    "SupportTicket",
    "TicketOrderingStrategy",
    "fifo_strategy",
    "filo_strategy",
    "main",
    "random_strategy",
]
```

This lets tests import from the package root rather than reaching into submodules.

### Imports

- Use **absolute imports** for cross-module references
  (`from patterns.behavioural.strategy.problem import SupportTicket`).
- Relative imports are allowed **only inside a single package** (e.g. a
  `support/` subpackage importing from a sibling module).
- All imports go at the **top of the file**. Never import inside a test or
  function body.

### `if __name__ == "__main__":`

Keep these blocks minimal — they should only call `main()`. They are excluded
from coverage globally via `pyproject.toml`; do **not** add `# pragma: no cover`
to them.

---

## Test conventions

### Directory structure mirrors the SUT (1:1)

For every SUT module `patterns/.../<variant>/<pkg>/<mod>.py`, there is a test
module at `patterns/.../tests/<variant>/<pkg>/test_<mod>.py`. The test tree is a
mirror image of the source tree, including `__init__.py` files.

```
strategy/
  problem/support/app.py
  solution_01/support/app.py
  tests/
    conftest.py            # cross-variant fixtures and helpers
    utils.py               # shared assertion helpers
    test_parity.py         # cross-variant behavioural parity
    problem/
      conftest.py
      test_main.py
      support/
        test_app.py
        test_ticket.py
    solution_01/
      conftest.py
      test_main.py
      support/
        test_app.py
        test_ticket.py
```

### 100% coverage, enforced

- `[tool.coverage.run].source` includes both the SUT directories **and** the
  `tests/` directory.
- `[tool.coverage.report].fail_under = 100`.
- Global `exclude_lines` covers `if __name__ == "__main__":`, `TYPE_CHECKING`,
  `@abstractmethod`, and `Protocol` ellipsis (`^\s*\.\.\.$`).

If you add code, add tests; if you can't cover a line, it shouldn't exist.

### No mocks. No trivial tests.

- **No `unittest.mock`, `pytest-mock`, or monkeypatching SUT internals.** Make
  the source deterministic instead.
- Don't write tests that only assert `X is not None`, that re-exports exist,
  that a dataclass has the field you just declared, or that `__str__` returns
  the string you literally just constructed. Test **behaviour**.

### Fixtures

- Every fixture has explicit type annotations on parameters and return type.
- Move all object instantiation into fixtures
  (`customer_support`, `support_ticket`, `support_tickets`, …). Tests that only
  call a function and assert on its return don't need a fixture; tests that
  build objects do.
- **Side-effect fixtures** (those that mutate state and return nothing) are
  prefixed with `_`, are typed `-> None`, and are consumed via
  `@pytest.mark.usefixtures("_name")`, never by parameter injection. Example:
  `_populate_tickets`.
- Inject fixtures by **default pytest mechanism** (function parameter). Do not
  `from .conftest import some_fixture`.
- Constants used by tests (sample data, expected messages) live as fixtures in
  `conftest.py`, not as module-level constants. This keeps them in coverage and
  forces a single source of truth.
- Helpers that aren't fixtures (e.g. assertion helpers) live in `tests/utils.py`,
  not in `conftest.py`.

### Parametrization

Use `pytest.param(..., id=...)` for human-readable IDs. Pass real callables and
real instances — not strings to be looked up:

```python
@pytest.fixture(
    params=[
        pytest.param(fifo_strategy, id="fifo"),
        pytest.param(filo_strategy, id="filo"),
        pytest.param(partial(random_strategy, seed=5), id="random-seed-5"),
    ],
)
def processing_strategy(request: pytest.FixtureRequest) -> TicketOrderingStrategy:
    return request.param
```

Avoid fixtures that shadow SUT functions just to "wrap" them; import the
function directly and put it in `pytest.param`.

### Assertions

- Assert **content, not shape**. Compare full lists/objects, not just lengths.
- For `capsys` output, assign to an `output` variable and use `in` for partial
  matches (`assert expected in output`). Don't reconstruct the expected string
  with helpers; partial matching is enough and is robust to trailing newlines.
- Move expected-value computation into fixtures so tests stay declarative
  (e.g. `expected_random_tickets`, `fifo_customer_order`).
- For ordering checks across stdout, use the shared
  `assert_customers_in_order(output, names)` helper from `tests/utils.py`.

### Test granularity

For any module that exposes multiple strategies/branches:

- Write **one test per strategy** that exercises the strategy in isolation.
- Plus **one parametrized test** (`test_*_all_strategies`) that exhausts every
  strategy through the public entry point.

The "problem" variant is special: because it's the reference for parity, its
per-strategy tests **also** assert output **order**, not just membership.

### Cross-variant parity

`tests/test_parity.py` runs every solution's `main()` and asserts its `capsys`
output equals the problem's. Whenever a new solution variant is added, append
it to the parametrization there.

---

## Adding a new pattern or variant — checklist

1. Create the SUT package with its own `__init__.py` re-exporting its public API.
2. Add a mirrored test directory: `tests/<variant>/...`, with `conftest.py`
   for variant-specific fixtures.
3. Add the SUT path to `[tool.coverage.run].source` in `pyproject.toml`.
4. If the variant introduces a new top-level pattern directory, scope the
   `format`/`lint`/`check` poe tasks accordingly.
5. Add a parity entry to `tests/test_parity.py` if applicable.
6. Run `uv run poe check && uv run poe test-cov` and verify 100% coverage.
7. **Update this file** if the variant introduces any new convention.

---

## Keeping AGENTS.md up to date

This file is the source of truth for agent-facing conventions. **Treat it like
code**: stale conventions are bugs.

**When you must update this file (in the same PR/change):**

1. A new tool, command, or `poe` task is added or renamed.
2. A new test, typing, fixture, import, or naming convention is agreed on
   (in review, in chat, or by precedent set in committed code).
3. An existing convention is changed, relaxed, tightened, or removed.
4. A new pattern category, variant, or top-level directory is added.
5. A Python version, dependency, or coverage target changes.
6. A previously implicit rule is made explicit because an agent or contributor
   got it wrong.

**How to update it:**

- Edit the relevant section directly. Prefer editing existing sections over
  appending new ones.
- Keep examples minimal and concrete; cite real files only when stable.
- If a rule has an exception, document the exception **next to** the rule
  (see "problem variant" notes under [Test granularity](#test-granularity)).
- Remove obsolete guidance — don't leave it behind "deprecated" headers.
- Bump the **Last reviewed** date below whenever you touch the file.

**Agent instructions:** Before finishing any task that introduces a new
convention, re-read this file and update it. If you're unsure whether
something qualifies as a "new convention", err on the side of documenting it.
The corresponding user-level skills (`python-test-structure`,
`python-pytest-fixtures`, `python-modern-typing`, `python-uv-poe-ruff`) should
be kept in sync with this file; if you change a rule here, update the
matching skill in the same change.

---

_Last reviewed: 2026-05-17_
