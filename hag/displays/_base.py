from abc import abstractmethod
from typing import List, Optional, Union

from ..parsers._base import Parser
from ..type_specs import Hotkeys, HotkeysWithModes


class Display:
    def __init__(
        self,
        hotkeys: Union[HotkeysWithModes, Hotkeys],
        parser: Parser,
    ):
        self.hotkeys = hotkeys
        self.parser = parser

    @abstractmethod
    def show(self, modes: Optional[Union[List[str], str]] = None):
        """Display the hotkeys.

        Args:
            modes: mode filter if `has_modes` is True.
        """
        pass
