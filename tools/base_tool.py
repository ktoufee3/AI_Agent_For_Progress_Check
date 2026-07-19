from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""
    description = ""

    @abstractmethod
    def execute(self, **kwargs):
        pass