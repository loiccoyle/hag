import os
from pathlib import Path
from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Sioyek(Parser):
    required = bool(Command("sioyek"))
    sources = {
        "system": [File(Path("/etc/sioyek/keys.config"))],
        "user": [
            File(
                Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
                / "sioyek"
                / "keys_user.config"
            )
        ],
    }
    has_modes = False

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        out = {}
        for _, contents in fetched.items():
            for content in contents:
                content = content.split("\n")
                for line in content:
                    if line.startswith("#") or len(line.strip()) == 0:
                        continue
                    (command, key) = line.split()
                    out[key] = command
        return out
