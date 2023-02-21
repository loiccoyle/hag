from abc import abstractmethod
from typing import Any, List, Optional, Union

from ..parsers._base import Parser
from ..type_specs import Hotkeys, HotkeysWithModes

DisplayContent = Any


class Display:
    def __init__(
        self,
        hotkeys: Union[HotkeysWithModes, Hotkeys],
        parser: Parser,
    ):
        self.hotkeys = hotkeys
        self.parser = parser

    def parse_modes(
        self, modes: Optional[Union[List[str], str]]
    ) -> Union[Hotkeys, HotkeysWithModes]:
        """Filter the hotkeys based on the requested modes."""
        if self.parser.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            return {mode: self.hotkeys[mode] for mode in modes}  # type: ignore
        else:
            return self.hotkeys

    @abstractmethod
    def format(self, modes: Optional[Union[List[str], str]] = None) -> DisplayContent:
        """Format the hotkeys for display."""
        pass

    @abstractmethod
    def show(self, content: DisplayContent) -> None:
        """Display the hotkeys.

        Args:
            content: the content to display.
        """
        pass


class DisplayText:
    @abstractmethod
    def format(self, modes: Optional[Union[List[str], str]] = None) -> str:
        pass

    def show(self, content: str) -> None:
        print(content)
