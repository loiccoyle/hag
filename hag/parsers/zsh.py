from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command


class Zsh(Parser):
    required = [Command("zsh")]
    # TODO: this doesn't work for my setup, my config is not sourced :(
    sources = {"user": [Command("zsh -ci bindkey")]}
    has_modes = False

    @staticmethod
    def _clean_key(string: str):
        string = string.replace('"', "")
        return string

    def extract(self, fetched) -> Hotkeys:
        content = fetched["user"][0]
        out = {}
        for line in content.split("\n"):
            if line:
                key, action = line.split(" ")
                out[self._clean_key(key)] = action
        return out
