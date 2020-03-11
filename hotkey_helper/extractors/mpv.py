import re
import os

from pathlib import Path

from .base import Extractor
from .base import CommandCheck
from .base import FileFetch
from .base import Command
from .base import File


# need to add custom config bindings

class Mpv(Extractor):
    required = [Command('mpv')]
    sources = {'system': [File('/usr/share/doc/mpv/input.conf'),
                          File('/etc/mpv/input.conf'),
                          File('/usr/local/etc/mpv/input.conf')],
                 'user': [File(Path(os.environ['XDG_CONFIG_HOME']) / 'mpv' / 'input.conf')]}
    has_modes = False

    @staticmethod
    def _clean_action(string):
        return string

    @staticmethod
    def _clean_key(string):
        return string[1:]

    def _extract(self):
        out = {}
        line_ignore = re.compile(r'#\S')
        line_remove = re.compile(r'#default-bindings.*')
        for content in self.fetched.values():
            if content:
                content = re.sub(line_remove, '', content[0])
                for line in content.split('\n'):
                    if re.match(line_ignore, line) :
                        line_split = line.split()
                        key = self._clean_key(line_split[0])
                        action = self._clean_action(' '.join(line_split[1:]))
                        out[key] = action
        return out

