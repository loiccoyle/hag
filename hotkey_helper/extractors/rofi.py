from .base import Extractor
from .base import CommandCheck
from .base import SectionExtract
from .base import ManPageFetch


class Rofi(SectionExtract, ManPageFetch, CommandCheck, Extractor):
    cmd = 'rofi'
    has_modes = False

    @staticmethod
    def _clean_action(string):
        string = string.replace('\\fB', '').replace('\\fR', '')
        string = string.replace('\\', '')
        if string[-1] != '.':
            string += '.'
        return string.strip()

    @staticmethod
    def _clean_keys(string):
        string = string.replace('\-', '-').replace('\\fB', '').replace('\\fR', '')
        return string

    def _extract(self):
        ht_section = self.find_sections(self.fetched,
                                        pattern='\.SH')['KEY BINDINGS']
        out = {}
        for line in ht_section.split('\n'):
            if line.startswith('\\fB') and 'has the following key bindings' not in line:
                line_split = line.split(':')
                key = self._clean_keys(line_split[0])
                action = self._clean_action(line_split[1])
                out[key] = action
        return out

