import os
import re
from pathlib import Path

from .base import Extractor
from .base import Command
from .base import File


class Sxhkd(Extractor):
    required = [Command("sxhkd")]
    sources = {
        "user": [File(Path(os.environ["XDG_CONFIG_HOME"]) / "sxhkd" / "sxhkdrc")]
    }
    had_modes = False

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

    def _extract(self):
        fetched = self._clean_fetched(self.fetched["user"][0])
        fetched = iter(fetched)
        return {
            self._clean_key(key): self._clean_action(next(fetched)) for key in fetched
        }
