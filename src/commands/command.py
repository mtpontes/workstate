from abc import ABC, abstractmethod


class CommandI(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
