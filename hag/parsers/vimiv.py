from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import PythonModule


class Vimiv(Parser):
    required = [PythonModule("vimiv")]
    has_modes = True

    def fetch(self) -> HotkeysWithModes:
        from vimiv import api

        return {mode: dict(keys) for mode, keys in api.keybindings.items()}  # type: ignore

    def parse(self, fetched: HotkeysWithModes) -> HotkeysWithModes:
        return fetched
