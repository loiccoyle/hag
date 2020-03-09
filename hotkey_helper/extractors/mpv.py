import re

from .base import Extractor
from .base import CommandCheck
from .base import SectionExtract
from .base import ManPageFetch

# need to add custom config bindings

class Mpv(SectionExtract, ManPageFetch, CommandCheck, Extractor):
    cmd = 'mpv'
    has_modes = False

    @staticmethod
    def _clean_action(string):
        string = string.replace('\\-', '-').replace('\n', ' ')
        string = re.sub(r'(\\fB)|(\\fR)|(\.TP)|(\\fP)|(\.UNINDENT.*)|(\\&)|( ?\(?[Ss]ee .*?[\.\)])', '', string)
        return string.rstrip()

    @staticmethod
    def _clean_key(string):
        string = re.sub('\\(ga', '`', string)
        string = re.sub('(\\\&)|(\\\)', '', string)
        string = re.sub(r' and ', ', ', string)
        return string

    def _extract(self):
        ht_section = self.find_sections(self.fetched,
                                        pattern='\.SS')['Keyboard Control']
        keys = self.find_sections(ht_section, pattern='\.B')
        out = {}
        for key, action in keys.items():
            key = self._clean_key(key)
            action = self._clean_action(action)
            out[key] = action
        return out

