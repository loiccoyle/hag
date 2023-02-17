import os
import re
from pathlib import Path
from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command, File, ManPage


class Sxiv(Parser):
    required = bool(Command("sxiv"))
    sources = {
        "default": [ManPage("sxiv")],
        "key_handler": [
            File(
                Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / "/.config"))
                / "sxiv"
                / "exec"
                / "key-handler"
            )
        ],
    }
    has_modes = True

    @staticmethod
    def _clean_action(string: str) -> str:
        return string.replace("\n", " ").strip()

    @staticmethod
    def _clean_key(string: str) -> str:
        return string.replace(r"\-", "-").strip()

    def parse(self, fetched: Dict[str, List[str]]) -> HotkeysWithModes:
        content = fetched["default"][0]
        # to select section from manpage
        content_section = re.compile(r"\.SH KEYBOARD COMMANDS.*?\.SH", re.DOTALL)
        # to split the section in different mode
        content_modes = re.compile(r"\.SS\s(.*?)\n(.*?)(?=(\.SS)|$)", re.DOTALL)
        # get each key/action from the mode section
        mode_key_action = re.compile(r"\.B[R]?\s(.*?\n)(.*?)(=?\.TP\n)", re.DOTALL)
        # clean up some stray strings
        content_clean = re.compile(r'(", ")|(\.I[R]? )')
        # only keep the desired man page section
        match = re.search(content_section, content)
        if match is None:
            raise TypeError("Section match is None")
        content = match[0]
        # clean
        content = re.sub(content_clean, "", content)
        out = {}
        # find all the modes
        for mode_match in re.finditer(content_modes, content):
            mode = mode_match[1]
            mode_c = mode_match[2]
            # add mode
            if mode not in out.keys():
                out[mode] = {}
            # find all the key/actions
            for key_action in re.finditer(mode_key_action, mode_c):
                key = self._clean_key(key_action[1])
                action = self._clean_action(key_action[2])
                out[mode][key] = action

        # parse key_handler
        if fetched["key_handler"]:
            out["key-handler"] = {}
            content = fetched["key_handler"][0]
            # remove comments
            comments = re.compile(r"\s*#.*")
            # get key/action
            content_cases = re.compile(r"\s\"(.*)\"\)\s*\n\s*(.*(?=;;))")
            # clean
            content = re.sub(comments, "", content)
            cases = re.finditer(content_cases, content)
            for case in cases:
                out["key-handler"][case[1]] = case[2]
        return out
