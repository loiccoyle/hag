import subprocess

from .base import Extractor
from .base import ManPageFetch
from .base import CommandCheck
from .base import GroffExtract



class Zathura(GroffExtract, ManPageFetch, CommandCheck, Extractor):
    cmd = 'zathura'
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
        ht_section = self.find_sections(self.fetched,
                                        pattern='\.SH')['MOUSE AND KEY BINDINGS']
        modes = self.find_sections(ht_section, pattern='\.sp')
        for m in modes.keys():
            keys = [self.split_title(k) for k in self.find_between(modes[m], '\.B')]
            keys = [(self._clean_key(k), self._clean_action(a)) for k, a in keys]
            modes[m] = dict(keys)
        return modes

