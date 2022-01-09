import re

from ..type_specs import HotkeysWithModes
from .base import Extractor
from .sources import Command


# TODO: this is broken
class Lazygit(Extractor):
    required = [Command("lazygit")]
    sources = {"user": [Command("lazygit -c")]}
    has_modes = True

    def extract(self, fetched) -> HotkeysWithModes:
        out = {}
        section_re = re.compile(r"(?<=keybinding:).*(?=os)", re.DOTALL)
        mode_re = re.compile(r"^  (\S*?):$", re.MULTILINE)
        key_action_re = re.compile(r"^    (\S*?): [\"']?(\S*?)[\"']?$", re.MULTILINE)
        # keep the keybinding section
        match = re.search(section_re, fetched["user"][0])
        if match is None:
            raise TypeError("Section match is None")
        content = match[0]
        for line in content.split("\n"):
            # get the mode
            mode_match = re.match(mode_re, line)
            if mode_match:
                mode = mode_match[1]
                out[mode] = {}
            else:
                # get the key/action
                key_action_match = re.match(key_action_re, line)
                if key_action_match:
                    out[mode][key_action_match[1]] = key_action_match[2]
        return out
