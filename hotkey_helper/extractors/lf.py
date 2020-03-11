import re
import os
from pathlib import Path

from .base import Extractor
from .base import Command
from .base import File


class Lf(Extractor):
    required = [Command('lf')]
    sources = {'default': [Command('lf -doc')],
               'user': [File(Path(os.environ['XDG_CONFIG_HOME']) / 'lf' / 'lfrc')]}
    has_modes = False

    @staticmethod
    def _clean_key(string):
        return string.replace("'", '').replace(')', '')

    def _extract(self):
        line_match = re.compile(r"\s.*?((\(default ')|([^c]map))")
        content_section = re.compile(r'Reference.*Configuration', re.DOTALL)
        out = {}
        # extract the default bindings
        fetched = re.search(content_section, self.fetched['default'][0])[0]
        for line in fetched.split('\n'):
            if re.match(line_match, line) and not 'string' in line:
                line_split = line.split()
                if line.lstrip().startswith('map'):
                    key = line_split[1]
                    action = ' '.join(line_split[2:])
                else:
                    key = self._clean_key(' '.join(line_split[2:]))
                    action = line_split[0]
                out[key] = action

        # extract the user bindings
        if self.fetched['user']:
            user = self.fetched['user'][0]
            for line in user.split('\n'):
                if line.lstrip().startswith('map'):
                    line_split = line.split()
                    key = line_split[1]
                    action = ' '.join(line_split[2:])
                    out[key] = action
        return out
