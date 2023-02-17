from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command


class Bash(Parser):
    required = bool(Command("bash"))
    sources = {"user": [Command("bash -ci 'bind -p'")]}
    has_modes = False

    @staticmethod
    def _clean_key(key: str) -> str:
        key = key.replace(r"\e", "alt+")
        key = key.replace(r"\C-", "ctrl+")
        key = key.replace(r"\\", "\\")
        return key

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        content = fetched["user"][0]
        out = {}
        for line in content.split("\n"):
            if line.startswith("#") or not line or "self-insert" in line:
                continue
            (key, action) = line.split(":")
            out[self._clean_key(key)] = action
        return out
