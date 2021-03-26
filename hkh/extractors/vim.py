import re
from tempfile import mkstemp

from .base import Extractor
from .base import Command
from .base import File


class Vim(Extractor):
    _temp_file = mkstemp()[1]
    required = [Command("vim")]
    # map won't show autocmd added hotkeys
    # kinda weird, the first command creates the file for the second source
    sources = {
        "user": [
            Command(f'vim -c "redir! > {_temp_file} | silent map | redir END | q"'),
            File(_temp_file),
        ]
    }
    has_modes = True

    def extract(self, fetched):
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
        content = fetched["user"][1]
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
