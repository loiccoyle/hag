
from .base import Extractor
from .base import ManPageFetch
from .base import CommandCheck
from .base import GroffExtract
from ..util import check_cmd


class Sxiv(GroffExtract, ManPageFetch, CommandCheck, Extractor):
    cmd = 'sxiv'
    has_modes = True

    @staticmethod
    def _clean_action(string):
        string = string.replace('\" , \" ', '')
        if '\n' in string:
            string = string[:string.index('\n')]
        return string

    @staticmethod
    def _clean_key(string):
        string = string.replace('\", \" ', '')
        string = string.replace('^', 'ctrl+').replace(' \\- ', '-').replace('\\(aq', '\'')
        string = ', '.join(string.split())
        return string

    def _extract(self):
        ht_section = self.find_sections(self.fetched,
                                        pattern='\.SH')['KEYBOARD COMMANDS']
        modes = self.find_sections(ht_section, pattern='\.SS')
        # uniform key anchors
        for m, content in modes.items():
            content = content.replace('.BR', '.B')
            keys = [self.split_title(k) for k in self.find_between(content, '\.B')]
            keys = [(self._clean_key(k), self._clean_action(a)) for k, a in keys]
            modes[m] = dict(keys)
        return modes

