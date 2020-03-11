import subprocess

from .base import Extractor
from .base import SectionExtract
from .base import Command
from .base import Manpage



class Zathura(SectionExtract, Extractor):
    required = [Command('zathura')]
    sources = {'default': [Manpage('zathura')]}
    has_modes = True

    @staticmethod
    def _clean_action(string):
        string = string.replace('\\fB', '').replace('\\fP', '')
        string = string.replace('\\-', '-')
        string = string[:string.index('\n')] + '.'
        return string

    @staticmethod
    def _clean_key(string):
        string = string.replace('^', 'ctrl+').replace('\\-', '-').replace('\\(aq', '\'')
        return string

    def _extract(self):
        ht_section = self.find_sections(self.fetched['default'][0],
                                        pattern='\.SH')['MOUSE AND KEY BINDINGS']
        modes = self.find_sections(ht_section, pattern='\.sp')
        for m in modes.keys():
            keys = [self.split_title(k) for k in self.find_between(modes[m], '\.B')]
            keys = [(self._clean_key(k), self._clean_action(a)) for k, a in keys]
            modes[m] = dict(keys)
        return modes

