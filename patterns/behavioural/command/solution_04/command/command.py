from typing import Callable

UndoCommand = Callable[[], None]
Command = Callable[..., UndoCommand]
