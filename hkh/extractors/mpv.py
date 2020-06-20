import re
import os

from pathlib import Path

from .base import Extractor
from .base import Command
from .base import File


# need to add custom config bindings


class Mpv(Extractor):
    required = [Command("mpv")]
    sources = {
        "system": [
            File("/usr/share/doc/mpv/input.conf"),
            File("/etc/mpv/input.conf"),
            File("/usr/local/etc/mpv/input.conf"),
        ],
        "user": [File(Path(os.environ["XDG_CONFIG_HOME"]) / "mpv" / "input.conf")],
    }
    has_modes = False

    @staticmethod
    def _clean_action(string):
        # replace whitespaces with space
        string = re.sub(r"\s+", " ", string)
        return string

    def _extract(self):
        out = {}
        content_key_action = re.compile(r"^#(\S+)\s+(.*)\n", re.MULTILINE)
        # remove this stray line to make the regex easier
        line_remove = re.compile(r"#default-bindings.*")
        # extract from all the fetched files
        for content in sum(self.fetched.values(), []):
            if content:
                content = re.sub(line_remove, "", content)
                for match in re.finditer(content_key_action, content):
                    out[match[1]] = self._clean_action(match[2])
        return out
