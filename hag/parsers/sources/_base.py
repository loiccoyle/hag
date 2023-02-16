from abc import abstractmethod


# Content sources
class Source:
    @abstractmethod
    def fetch(self) -> str:
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        pass
