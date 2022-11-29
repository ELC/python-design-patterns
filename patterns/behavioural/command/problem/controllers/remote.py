from dataclasses import dataclass

from typing import Any, Optional

from ..heating import HeatingSystem

from ..command import Command


@dataclass
class RemoteController:
    heating_system: HeatingSystem
    command: Optional[tuple[Command, dict[str, Any]]] = None

    def add_command(self, command: Command, arguments: Optional[dict[str, Any]] = None):
        command_arguments = arguments if arguments else {}
        self.command = (command, command_arguments)

    def execute(self):
        if self.command is None:
            raise ValueError("No Commands Set")

        command, command_arguments = self.command
        if command is Command.TURN_ON:
            self.heating_system.turn_on(**command_arguments)
            return
        
        if command is Command.TURN_OFF:
            self.heating_system.turn_off(**command_arguments)
            return
        
        if command is Command.SET_TEMPERATURE:
            if "temperature" not in command_arguments:
                raise ValueError("Temperature must be provided")

            self.heating_system.target_temprature_in_celcius = command_arguments["temperature"]
            return
        
        raise ValueError(f"Unkown Command: {command}")
