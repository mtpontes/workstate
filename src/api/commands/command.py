from abc import ABC, abstractmethod


class CommandI(ABC):
    @abstractmethod
    def execute() -> None:
        pass
