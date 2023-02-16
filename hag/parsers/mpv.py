from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command, PythonModule


class Mpv(Parser):
    required = all([Command("mpv"), PythonModule("mpv")])
    has_modes = True

    def fetch(self) -> List[Dict[str, str]]:
        import mpv

        player = mpv.MPV()  # type: ignore
        out = player.input_bindings
        player.terminate()
        return out

    def parse(self, fetched: List[Dict[str, str]]) -> HotkeysWithModes:
        out = {}
        for binding in fetched:
            if binding["section"] not in out:
                out[binding["section"]] = {}
            out[binding["section"]][binding["key"]] = binding.get(
                "comment", binding.get("cmd")
            )
        return out
