from abc import ABC, abstractmethod


class StringPrompterI(ABC):
    @abstractmethod
    def prompt(self) -> str:
        pass
