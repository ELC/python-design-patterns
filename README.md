# Python Design Patterns

This repo is a collection of non-trivial examples of several design patterns
implemented in different ways. Its aim is to contrast *traditional* (i.e. GoF)
design patterns with more Pythonic equivalents.

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

To generate the metrics, use the following commands from the [radon library](https://pypi.org/project/radon/):

```
python -m radon raw . -s -O stats.md
python -m radon mi . -s -j -O mi.json
python -m radon cc . -s --show-closures --total-average --md -O complexity.md
```
