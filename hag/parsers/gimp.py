import os
from pathlib import Path
from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Gimp(Parser):
    required = bool(Command("gimp"))
    sources = {
        "system": [File(menurc) for menurc in (Path("/etc/gimp/").glob("**/menurc"))],
        "user": [
            File(menurc)
            for menurc in (
                Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
                / "GIMP"
            ).glob("**/menurc")
        ],
    }
    has_modes = False

    @staticmethod
    def _clean_key(key: str) -> str:
        return key.split("/")[-1]

    @staticmethod
    def _clean_line(line: str) -> str:
        if line.startswith(";"):
            line = line.replace(";", "")
        line = line.replace('"', "")
        line = line.replace("(", "").replace(")", "")
        return line

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        out = {}
        for _, sources in fetched.items():
            for content in sources:
                for line in content.split("\n"):
                    if "(gtk_accel_path" not in line:
                        continue
                    line = self._clean_line(line)
                    line = line.split()
                    if len(line) < 3:
                        continue
                    out[self._clean_key(line[1])] = line[2]
        return out
