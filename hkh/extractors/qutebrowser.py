import re
import os
from pathlib import Path

from .base import Extractor
from .base import Command
from .base import File


class Qutebrowser(Extractor):
    required = [Command("qutebrowser")]
    # TODO: figure out better way than parsing the config file. There should be away
    # to get the config from qutebrowser's python api.
    sources = {
        "user": [
            File(Path(os.environ["XDG_CONFIG_HOME"]) / "qutebrowser" / "config.py")
        ]
    }
    has_modes = True

    def _extract(self):
        fetched = self.fetched["user"][0]
        content_key_action = re.compile(
            r".*config.bind\([\'\"](.*?)[\'\"],\s*[\'\"](.*?)[\'\"](,\s*mode=[\'\"](.*?)[\'\"])?"
        )
        out = {}
        for match in re.finditer(content_key_action, fetched):
            # the mode kwargs default to normal
            if match[4]:
                mode = match[4]
            else:
                mode = "normal"
            if not mode in out.keys():
                out[mode] = {}
            out[mode][match[1]] = match[2]
        return out
