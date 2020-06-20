import re

from .base import Extractor
from .base import Command


class Rofi(Extractor):
    required = [Command("rofi")]
    sources = {"user": [Command("rofi -dump-config")]}
    has_modes = False

    @staticmethod
    def _clean_key(string):
        string = string.lstrip()[1:-1]
        return string

    def _extract(self):
        line_match = re.compile(r"(/\*)?\t((kb)|(me)|(ml))")
        line_clean = re.compile(r"((/\*)|(\*/)|(\t)|(;))")
        content_key_action = re.compile(r".*?(((kb)|(ml)|(me))-.*?):\s+\"(.*?)\"")
        content = self.fetched["user"][0]
        out = {}
        for match in re.finditer(content_key_action, content):
            out[match[6]] = match[1]
        return out
