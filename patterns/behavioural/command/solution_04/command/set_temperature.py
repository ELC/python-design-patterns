from typing import Protocol

from .command import UndoCommand


class SeteableTemperature(Protocol):

    @property
    def target_temprature_in_celcius(self) -> float:
        ...
    
    @target_temprature_in_celcius.setter
    def target_temprature_in_celcius(self, temperature: float) -> None:
        ...


def set_temperature_command(receiver: SeteableTemperature, target_temperature: float) -> UndoCommand:
    previous_temperature = receiver.target_temprature_in_celcius
    receiver.target_temprature_in_celcius = target_temperature

    def undo_set_temperature():
        receiver.target_temprature_in_celcius = previous_temperature

    return undo_set_temperature
