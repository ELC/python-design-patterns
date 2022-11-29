# Python Design Patterns


## Patterns

- [Strategy](./patterns/behavioural/strategy/README.md)
- [Bridge](./patterns/structural/bridge/README.md)
- [Observer](./patterns/behavioural/observer/README.md)
- [Iterator](./patterns/behavioural/iterator/README.md)
- [Command](./patterns/behavioural/command/README.md)


The commands to generate the metrics are base on the [radon library](https://pypi.org/project/radon/):

```
python -m radon raw . -s -O stats.md
python -m radon mi . -s -j -O mi.json
python -m radon cc .  -s --show-closures --total-average --md -O complexity.md
```
