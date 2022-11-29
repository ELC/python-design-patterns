# Python Design Patterns


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
