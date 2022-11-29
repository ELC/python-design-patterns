from typing import Protocol

from .command import Command


class Switchable(Protocol):
    
    def turn_on(self):
        ...
    
    def turn_off(self):
        ...


def turn_on_command(receiver: Switchable) -> Command:
    def inner():
        receiver.turn_on()

        return lambda: receiver.turn_off()

    return inner


def turn_off_command(receiver: Switchable) -> Command:
    def inner():
        receiver.turn_off()
        
        return lambda: receiver.turn_on()
    
    return inner
