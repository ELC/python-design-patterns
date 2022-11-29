from dataclasses import dataclass, field

from typing import Any, Optional

from ..heating import HeatingSystem

from ..command import Command


@dataclass
class IoTController:
    heating_system: HeatingSystem
    _history: list[Command] = field(default_factory=list)
    _undo_commands: list[tuple[Command, dict[str, Any]]] = field(default_factory=list)
    _command_queue: list[tuple[Command, dict[str, Any]]] = field(default_factory=list)

    def add_command(self, command: Command, arguments: Optional[dict[str, Any]] = None):
        command_arguments = arguments if arguments else {}
        self._command_queue.append((command, command_arguments))

    def execute(self):
        if not self._command_queue:
            raise ValueError("No commands are in queue")

        for command, command_arguments in self._command_queue:
            self._execute_command(command, command_arguments)
        self._command_queue = []
        
    def _execute_command(self, command: Command, command_arguments: dict[str, Any]):
        if command is Command.TURN_ON:
            self._undo_commands.append((Command.TURN_OFF, {}))
            self.heating_system.turn_on(**command_arguments)
            return
        
        if command is Command.TURN_OFF:
            self._undo_commands.append((Command.TURN_ON, {}))
            self.heating_system.turn_off(**command_arguments)
            return
        
        if command is Command.SET_TEMPERATURE:
            if "temperature" not in command_arguments:
                raise ValueError("Temperature must be provided")

            current_temperature = self.heating_system.target_temprature_in_celcius
            self._undo_commands.append((Command.SET_TEMPERATURE, {"temperature": current_temperature}))
            self.heating_system.target_temprature_in_celcius = command_arguments["temperature"]
            return
        
        raise ValueError(f"Unkown Command: {command}")


    def undo_last_command(self):
        if not self._undo_commands:
            return
        
        undo_command, undo_command_arguments = self._undo_commands.pop()

        self._execute_command(undo_command, undo_command_arguments)

        
    def undo_all_commands(self):
        for undo_command, undo_command_arguments in reversed(self._undo_commands):
            self._execute_command(undo_command, undo_command_arguments)
