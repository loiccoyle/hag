from typing import Dict

from .base import Extractor
from .sources import PythonModule


class Vimiv(Extractor):
    required = [PythonModule("vimiv")]
    has_modes = True

    def fetch(self) -> Dict[str, Dict[str, str]]:
        from vimiv import api

        return {mode: dict(keys) for mode, keys in api.keybindings.items()}

    def extract(self, fetched) -> Dict[str, Dict[str, str]]:
        return fetched
