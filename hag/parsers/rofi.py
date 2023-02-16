import re

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command


class Rofi(Parser):
    required = [Command("rofi")]
    sources = {"user": [Command("rofi -dump-config")]}
    has_modes = False

    @staticmethod
    def _clean_key(string):
        string = string.lstrip()[1:-1]
        return string

    def parse(self, fetched) -> Hotkeys:
        content_key_action = re.compile(r".*?(((kb)|(ml)|(me))-.*?):\s+\"(.*?)\"")
        content = fetched["user"][0]
        out = {}
        for match in re.finditer(content_key_action, content):
            out[match[6]] = match[1]
        return out
