import os
import re
from pathlib import Path
from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Sxhkd(Parser):
    required = bool(Command("sxhkd"))
    sources = {
        "user": [
            File(
                Path(
                    os.environ.get(
                        "XDG_CONFIG_HOME",
                        Path.home() / ".config",
                    )
                )
                / "sxhkd"
                / "sxhkdrc"
            )
        ]
    }
    has_modes = False

    @staticmethod
    def _clean_fetched(content: str) -> List[str]:
        # remove blank lines
        lines = [line for line in content.split("\n") if not re.match(r"\W?#", line)]
        lines = [line for line in lines if line != ""]
        return lines

    @staticmethod
    def _clean_action(string: str) -> str:
        string = string.strip()
        return string

    @staticmethod
    def _clean_key(string: str) -> str:
        string = string.replace(" + ", "+")
        return string

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        content = self._clean_fetched(fetched["user"][0])
        content = iter(content)
        out = {}
        for key in content:
            actions = []
            action = self._clean_action(next(content))
            actions.append(action)
            while action.endswith("\\"):
                action = self._clean_action(next(content))
                actions.append(action)
            out[self._clean_key(key)] = "".join(
                [ac.replace("//", "") for ac in actions]
            )
        return out
