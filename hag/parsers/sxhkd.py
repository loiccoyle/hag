import os
import re
from pathlib import Path

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Sxhkd(Parser):
    required = [Command("sxhkd")]
    sources = {
        "user": [
            File(
                Path(
                    os.environ.get(
                        "XDG_CONFIG_HOME",
                        Path(os.environ["HOME"]) / ".config",
                    )
                )
                / "sxhkd"
                / "sxhkdrc"
            )
        ]
    }
    has_modes = False

    @staticmethod
    def _clean_fetched(content):
        # remove blank lines
        lines = [line for line in content.split("\n") if not re.match(r"\W?#", line)]
        lines = [line for line in lines if line != ""]
        return lines

    @staticmethod
    def _clean_action(string):
        string = string.strip()
        return string

    @staticmethod
    def _clean_key(string):
        string = string.replace(" + ", "+")
        return string

    def parse(self, fetched) -> Hotkeys:
        fetched = self._clean_fetched(fetched["user"][0])
        fetched = iter(fetched)
        out = {}
        for key in fetched:
            actions = []
            action = self._clean_action(next(fetched))
            actions.append(action)
            while action.endswith("\\"):
                action = self._clean_action(next(fetched))
                actions.append(action)
            out[self._clean_key(key)] = "".join(
                [ac.replace("//", "") for ac in actions]
            )
        return out
