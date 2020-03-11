import os
import re

from pathlib import Path

from .base import Extractor
from .base import SectionExtract
from .base import File
from .base import Command
from .base import Manpage


class Sxiv(SectionExtract, Extractor):
    required = [Command('sxiv')]
    sources = {'default': [Manpage('sxiv')],
               'key_handler': [File(Path(os.environ['XDG_CONFIG_HOME']) / 'sxiv' / 'exec' / 'key-handler')]}
    has_modes = True

    @staticmethod
    def _clean_action(string):
        string = string.replace('\" , \" ', '').replace('.IR', '').replace('.I', '').replace('\n', '')
        if '.TP' in string:
            string = string[:string.index('.TP')]
        return string

    @staticmethod
    def _clean_key(string):
        return string.replace(' , ', ',').replace('\-', '-')

    @staticmethod
    def _clean_key_key_handler(string):
        return string.strip()[1:-2]


    @staticmethod
    def _clean_action_key_handler(string):
        return string.strip().replace(';', '')

    def _extract(self):
        ht_section = self.find_sections(self.fetched['default'][0],
                                        pattern='\.SH')['KEYBOARD COMMANDS']
        modes = self.find_sections(ht_section, pattern='\.SS')
        # uniform key anchors
        for m, content in modes.items():
            content = content.replace('.BR', '.B')
            keys = [self.split_title(k) for k in self.find_between(content, '\.B')]
            keys = [(self._clean_key(k), self._clean_action(a)) for k, a in keys]
            modes[m] = dict(keys)

        # extract key_handler
        if self.fetched['key_handler']:
            modes['key-handler'] = {}
            content = self.fetched['key_handler'][0]
            comments = re.compile(r'\s*#.*')
            content_cases = re.compile(r"(\s[^#]\".*\"\)\s*\n)(.*)")
            content = re.sub(comments, '', content)
            cases = re.finditer(content_cases, content)
            for case in cases:
                key = self._clean_key_key_handler(case[1])
                action = self._clean_action_key_handler(case[2])
                modes['key-handler'][key] = action
        return modes

