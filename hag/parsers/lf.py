import os
import re
from pathlib import Path
from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Lf(Parser):
    required = bool(Command("lf"))
    sources = {
        "default": [Command("lf -doc")],
        "user": [
            File(
                Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
                / "lf"
                / "lfrc"
            )
        ],
    }
    has_modes = False

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        content_clean = re.compile(r".*?((boolean)|(string)|(integer)).*\n")
        content_section = re.compile(r"Reference.*?Configuration", re.DOTALL)
        default_key_action = re.compile(r"\s*(.*?)\s*\(default (.*)\)")
        map_key_action = re.compile(r"\s*map\s(\w+)\s*(.*)\n")
        content_clean_quote = re.compile(r'(?<!")\'(?!")')
        # parse the default bindings
        # get the desired section
        match = re.search(content_section, fetched["default"][0])
        if match is None:
            raise TypeError("Section match is None.")
        content = match[0]
        # clean the problematic lines
        content = re.sub(content_clean, "", content)
        # remove the quotes could be improved
        content = re.sub(content_clean_quote, "", content)
        content = content.replace("'\"'", '"').replace('"\'"', "'")
        out = {}
        for match in re.finditer(default_key_action, content):
            out[match[2]] = match[1]

        for match in re.finditer(map_key_action, content):
            out[match[1]] = match[2]

        # parse the user bindings
        if fetched["user"]:
            content = fetched["user"][0]
            for match in re.finditer(map_key_action, content):
                out[match[1]] = match[2]
        return out
