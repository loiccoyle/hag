import re
import os

from .base import Extractor
from .base import Command


class Lazygit(Extractor):
    required = [Command("lazygit")]
    sources = {"user": [Command("lazygit -c")]}
    has_modes = True

    def _extract(self):
        out = {}
        section_re = re.compile(r"(?<=keybinding:).*", re.DOTALL)
        mode_re = re.compile(r"^  (\S*?):$", re.MULTILINE)
        key_action_re = re.compile(r"^    (\S*?): '(\S*?)'$", re.MULTILINE)
        content = re.search(section_re, self.fetched["user"][0])[0]
        # print(content)
        for line in content.split("\n"):
            mode_match = re.match(mode_re, line)
            if mode_match:
                mode = mode_match[1]
                out[mode] = {}
            else:
                key_action_match = re.match(key_action_re, line)
                if key_action_match:
                    out[mode][key_action_match[1]] = key_action_match[2]
        return out
