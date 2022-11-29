from dataclasses import dataclass
from typing import Protocol, Optional

from .command import Command


class SeteableTemperature(Protocol):

    @property
    def target_temprature_in_celcius(self) -> float:
        ...
    
    @target_temprature_in_celcius.setter
    def target_temprature_in_celcius(self, temperature: float) -> None:
        ...


@dataclass       
class SetTemperatureCommand(Command[SeteableTemperature]):
    target_temperature: float
    previous_temperature: Optional[float] = None

    def execute(self) -> None:
        self.previous_temperature = self.receiver.target_temprature_in_celcius
        self.receiver.target_temprature_in_celcius = self.target_temperature

    def undo(self):
        if self.previous_temperature is None:
            raise ValueError("Can only undo commands that were executed")
        self.receiver.target_temprature_in_celcius = self.previous_temperature