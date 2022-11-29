# Python Design Patterns

This repo is a collection of non-trivial examples of several design patterns
implemented in different ways. Its aim is to contrast *traditional* (i.e. GoF)
design patterns with more Pythonic equivalents, metrics about each
implementation are also provided.

The notion of being Pythonic is indeed subjective and it is used in the sense
of leveraging built-in Python features such as Protocols, Callable classes,
closures, partial evaluation, generators, decorators, first-class functions and
so on.

Each pattern has an independent README linked below with a guide to highlight
differences between implementation details.

## Patterns

### Behavioural

- [Strategy](./patterns/behavioural/strategy/README.md)
- [Observer](./patterns/behavioural/observer/README.md)
- [Iterator](./patterns/behavioural/iterator/README.md)
- [Command](./patterns/behavioural/command/README.md)

### Creational

### Structural

- [Bridge](./patterns/structural/bridge/README.md)

## Metrics

The metrics to be used are:

- Cyclomatic Complexity: is equal to the number of linearly independent paths through the code.
- Maintainability Index: is calculated as a factored formula consisting of SLOC, Cyclomatic Complexity and Halstead volume.
- LOC: The total number of lines of code. It does not necessarily correspond to the number of lines in the file.
- LLOC: The number of logical lines of code. Every logical line of code contains exactly one statement.
- SLOC: The number of source lines of code - not necessarily corresponding to the LLOC.

To generate the metrics, use the following commands from the [radon library](https://pypi.org/project/radon/):

```
python -m radon raw . -s -O stats.md
python -m radon mi . -s -j -O mi.json
python -m radon cc . -s --show-closures --total-average --md -O complexity.md
```
