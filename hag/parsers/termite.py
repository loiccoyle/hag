import re
from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command, ManPage


class Termite(Parser):
    required = bool(Command("termite"))
    sources = {"default": [ManPage("termite")]}
    has_modes = True

    def parse(self, fetched: Dict[str, List[str]]) -> HotkeysWithModes:
        content = fetched["default"][0]
        # remove some stray groff tags
        content_clean = re.compile(r"(\\f[PBI])")
        # get the desired section
        content_section = re.compile(r"\.SH KEYBINDINGS.*?\.SH", re.DOTALL)
        # split the section into modes
        content_modes = re.compile(r"\.SS\s+(.*?)\n(.*?)(?=\.SS|$)", re.DOTALL)
        # get the key/actions
        mode_key_action = re.compile(r'\.IP\s+"(.*?)"\n(.*?)\n')
        # clean
        content = re.sub(content_clean, "", content)
        # get section
        match = re.search(content_section, content)
        if match is None:
            raise TypeError("Section match is None")
        content = match[0]
        out = {}
        # find modes
        for mode_match in re.finditer(content_modes, content):
            mode = mode_match[1]
            mode_content = mode_match[2]
            if mode not in out.keys():
                out[mode] = {}
            # find keys
            for key_action in re.finditer(mode_key_action, mode_content):
                out[mode][key_action[1]] = key_action[2]
        return out
