import re

from ..type_specs import HotkeysWithModes
from .base import Extractor
from .sources import Command


class Vim(Extractor):
    required = [Command("vim")]
    # map won't show autocmd added hotkeys
    sources = {
        "user": [
            Command(f'vim -e +"redir >> /dev/stdout | map | redir END" -scq'),
        ]
    }
    has_modes = True

    def extract(self, fetched) -> HotkeysWithModes:
        # convert vim mode notation to human, from :help map
        mode_map = {
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
        content = fetched["user"][0]
        # get the key/action
        content_key_action = re.compile(r"(.)\s+(\S+)\s+[@\&\*]?\s*(.*?)\n")
        out = {}
        for match in re.finditer(content_key_action, content):
            key = match[2]
            # remove <Plug> keys
            if not key.startswith("<Plug>"):
                mode = mode_map[match[1]]
                action = match[3]
                if not mode in out.keys():
                    out[mode] = {}
                out[mode][key] = action
        return out
