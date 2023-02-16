from abc import abstractmethod


# Content sources
class Source:
    @abstractmethod
    def fetch(self) -> str:
        """Fetch the content of the source."""
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        """Return true if the source is available, false otherwise."""
        pass
