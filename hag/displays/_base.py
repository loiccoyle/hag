from abc import abstractmethod
from typing import List, Optional, Union

from ..type_specs import Hotkeys, HotkeysWithModes


class Display:
    def __init__(self, hotkeys: Union[HotkeysWithModes, Hotkeys], has_modes: bool):
        self.hotkeys = hotkeys
        self.has_modes = has_modes

    @abstractmethod
    def show(self, modes: Optional[Union[List[str], str]] = None):
        """Display the hotkeys.

        Args:
            modes: mode filter if `has_modes` is True.
        """
        pass
