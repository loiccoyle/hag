import re
import os
from pathlib import Path

from .base import Extractor
from .base import CommandCheck
from .base import FileFetch

class Qutebrowser(FileFetch, CommandCheck, Extractor):
    cmd = 'qutebrowser'
    has_modes = True
    if 'XDG_CONFIG_HOME' in os.environ.keys():
        file_path = Path(os.environ['XDG_CONFIG_HOME']) / 'qutebrowser' / 'config.py'
    else:
        file_path = Path(os.environ['HOME']) / '.config' / 'qutebrowser' / 'config.py'

    @staticmethod
    def _clean_fetched(content):
        return [line for line in content.split('\n') if 'config.bind' in line]

    @staticmethod
    def _clean_key(string):
        return string[1: -1]

    @staticmethod
    def _clean_action(string):
        return string[1: -1]

    @staticmethod
    def _clean_mode(string):
        return string.split('=')[-1][1: -1]

    def _extract(self):
        fetched = self._clean_fetched(self.fetched)
        out = {}
        for line in fetched:
            line = re.search(r"(?<=\().*?(?=\))", line)[0].split(', ')
            if len(line) < 3:
                line += ["mode='normal'"]
            mode = self._clean_mode(line[2])
            action = self._clean_action(line[1])
            key = self._clean_key(line[0])
            if mode not in out.keys():
                out[mode] = {}
            out[mode][key] = action
        return out

