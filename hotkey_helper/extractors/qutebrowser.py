import re
import os
from pathlib import Path

from .base import Extractor
from .base import CommandCheck
from .base import FileFetch
from .base import Command
from .base import File

class Qutebrowser(Extractor):
    required = [Command('qutebrowser')]
    sources = {'user': [File(Path(os.environ['XDG_CONFIG_HOME']) / 'qutebrowser' / 'config.py')]}

    has_modes = True

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
        fetched = self._clean_fetched(self.fetched['user'][0])
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

