from dataclasses import dataclass
from typing import Protocol

from .command import Command

class Switchable(Protocol):
    
    def turn_on(self):
        ...
    
    def turn_off(self):
        ...


@dataclass
class TurnOnCommand(Command[Switchable]):
    def execute(self):
        self.receiver.turn_on()

    def undo(self):
        self.receiver.turn_off()


@dataclass
class TurnOffCommand(Command[Switchable]):
    def execute(self):
        self.receiver.turn_off()
    
    def undo(self):
        self.receiver.turn_on()

