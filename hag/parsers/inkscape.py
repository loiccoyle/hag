import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

from ..type_specs import Hotkeys
from ._base import Parser
from .sources import Command, File


class Inkscape(Parser):
    required = bool(Command("inkscape"))
    sources = {
        "system": [File(Path("/usr/share/inkscape/keys/default.xml"))],
        "user": [
            File(
                Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
                / "inkscape"
                / "keys"
                / "default.xml"
            )
        ],
    }
    has_modes = False

    @staticmethod
    def _clean_key(key: str) -> str:
        key = re.sub(r"\s+", "", key)
        return key

    def parse(self, fetched: Dict[str, List[str]]) -> Hotkeys:
        out = {}
        for _, sources in fetched.items():
            for content in sources:
                tree = ET.fromstring(content)
                for bind in tree.findall("bind"):
                    # print(bind.attrib)
                    if "keys" in bind.attrib:
                        out[self._clean_key(bind.attrib["keys"])] = bind.attrib[
                            "gaction"
                        ]
        return out
