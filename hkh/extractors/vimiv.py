from ..type_specs import HotkeysWithModes
from .base import Extractor
from .sources import PythonModule


class Vimiv(Extractor):
    required = [PythonModule("vimiv")]
    has_modes = True

    def fetch(self) -> HotkeysWithModes:
        from vimiv import api

        return {mode: dict(keys) for mode, keys in api.keybindings.items()}

    def extract(self, fetched) -> HotkeysWithModes:
        return fetched
