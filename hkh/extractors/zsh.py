import re

from .base import Extractor
from .base import Command


class Zsh(Extractor):
    required = [Command("zsh")]
    sources = {"user": [Command("zsh -c bindkey")]}
    has_modes = False

    @staticmethod
    def _clean_key(string):
        string = string.replace('"', "")
        return string

    def extract(self, fetched):
        content = fetched["user"][0]
        out = {}
        for line in content.split("\n"):
            if line:
                key, action = line.split(" ")
                out[self._clean_key(key)] = action
        return out
