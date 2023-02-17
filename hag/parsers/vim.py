import re
from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command

MODE_MAP: Dict[str, str] = {
    " ": "Normal, Visual, Select, Operator-pending",
    "n": "Normal",
    "v": "Visual, Select",
    "s": "Select",
    "x": "Visual",
    "o": "Operator-pending",
    "!": "Insert, Command-line",
    "i": "Insert",
    "l": '":lmap" mappings for Insert, Command-line and Lang-Arg',
    "c": "Command-line",
    "t": "Terminal-Job",
}


class Vim(Parser):
    required = bool(Command("vim"))
    # map won't show autocmd added hotkeys
    sources = {
        "user": [
            Command('vim -e +"redir >> /dev/stdout | map | redir END" -scq'),
        ]
    }
    has_modes = True

    def parse(self, fetched: Dict[str, List[str]]) -> HotkeysWithModes:
        # convert vim mode notation to human, from :help map
        content = fetched["user"][0]
        # get the key/action
        content_key_action = re.compile(r"(.)\s+(\S+)\s+[@\&\*]?\s*(.*?)\n")
        out = {}
        for match in re.finditer(content_key_action, content):
            key = match[2]
            # remove <Plug> keys
            if not key.startswith("<Plug>"):
                mode = MODE_MAP[match[1]]
                action = match[3]
                if mode not in out.keys():
                    out[mode] = {}
                out[mode][key] = action
        return out
