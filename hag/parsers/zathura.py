import re
from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser, SectionParse
from .sources import Command, ManPage


class Zathura(SectionParse, Parser):
    required = bool(Command("zathura"))
    sources = {"default": [ManPage("zathura")]}
    has_modes = True

    @staticmethod
    def _clean_action(string: str) -> str:
        string = string.replace("\\fB", "").replace("\\fP", "")
        string = string.replace("\\-", "-")
        string = string[: string.index("\n")] + "."
        return string

    @staticmethod
    def _clean_key(string: str) -> str:
        string = string.replace("\\-", "-").replace("\\(aq", "'")
        return string

    def parse(self, fetched: Dict[str, List[str]]) -> HotkeysWithModes:
        content = fetched["default"][0]
        # select section from manpage
        content_section = re.compile(r"\.SH MOUSE AND KEY BINDINGS.*?\.SH", re.DOTALL)
        # split section in modes
        content_modes = re.compile(r"\.sp\n(.*?)\n(.*?)(?=\.sp|$)", re.DOTALL)
        # get the key/actions
        mode_key_action = re.compile(r"\.B(.*?)\n(.*?)\n")
        match = re.search(content_section, content)
        if match is None:
            raise TypeError("Section match is None")
        content = match[0]
        out = {}
        for mode_match in re.finditer(content_modes, content):
            mode = mode_match[1]
            mode_content = mode_match[2]
            if mode not in out.keys():
                out[mode] = {}
            for key_action in re.finditer(mode_key_action, mode_content):
                key = self._clean_key(key_action[1])
                out[key] = key_action[2]
        return out
