import os
import re
from pathlib import Path

from .base import Extractor
from .base import CommandCheck
from .base import FileFetch


class Sxhkd(FileFetch, CommandCheck, Extractor):
    cmd = 'sxhkd'
    had_modes = False
    if 'XDG_CONFIG_HOME' in os.environ:
        file_path = Path(os.environ['XDG_CONFIG_HOME']) / 'sxhkd' / 'sxhkdrc'
    else:
        file_path = Path(os.environ['HOME']) / 'sxhkd' / 'sxhkdrc'

    @staticmethod
    def _clean_fetched(content):
        # remove blank lines
        lines = [line for line in content.split('\n') if not re.match(r'\W?#', line)]
        lines = [line for line in lines if line != '']
        return lines

    @staticmethod
    def _clean_action(string):
        string = string.strip()
        return string

    @staticmethod
    def _clean_key(string):
        string = string.replace(' + ', '+')
        return string

    def _extract(self):
        fetched = self._clean_fetched(self.fetched)
        fetched = iter(fetched)
        return {self._clean_key(key): self._clean_action(next(fetched)) for key in fetched}

