from dataclasses import dataclass, field
from enum import Enum, auto


class PowerState(Enum):
    ON = auto()
    OFF = auto()


@dataclass
class HeatingUnit:
    name: str
    state: PowerState = PowerState.OFF
    target_temperature_in_celcius: float = 22


@dataclass
class HeatingSystem:
    units: list[HeatingUnit] = field(default_factory=list)
    _target_temperature_in_celcius: float = 22
    _state: PowerState = PowerState.OFF

    @property
    def target_temprature_in_celcius(self) -> float:
        return self._target_temperature_in_celcius
    
    @target_temprature_in_celcius.setter
    def target_temprature_in_celcius(self, temperature: float):
        self._target_temperature_in_celcius = temperature
        for unit in self.units:
            unit.target_temperature_in_celcius = temperature

    @property
    def state(self) -> PowerState:
        return self._state
    
    @state.setter
    def state(self, state: PowerState):
        self._state = state
        for unit in self.units:
            unit.state = state

    def turn_on(self):
        self.state = PowerState.ON

    def turn_off(self):
        self.state = PowerState.OFF