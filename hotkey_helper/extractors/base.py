import re
import gzip
import subprocess

from types import GeneratorType
from abc import abstractmethod

from ..util import check_cmd


class Extractor:
    has_modes = None  # boolean

    def __init__(self):
        pass

    @abstractmethod
    def _fetch(self):
       pass

    def fetch(self):
        self.fetched = self._fetch()
        return self

    @abstractmethod
    def _extract(self):
        '''Must return a dict with structure:
           if has_modes: {'mode': {'hotkey': 'action'}}
           else: {'hotkey': 'action'}
        '''
        pass

    def extract(self):
        self.extracted = self._extract()
        return self


class ManPageFetch:
    def _fetch(self):
        man_page_path = subprocess.check_output(['man', '-w', self.cmd]).decode('utf8')
        man_page_path = man_page_path.rstrip()
        with gzip.open(man_page_path, 'rb') as gfp:
            lines = gfp.read()
        return lines.decode('utf8')

class FileFetch:
    def __init__(self):
        super().__init__()
        if not self.file_path.is_file():
            raise OSError(f'{self.file_path} does not exist.')

    def _fetch(self):
        with open(self.file_path, 'r') as fp:
            lines = fp.read()
        return lines


class CommandCheck:
    def __init__(self):
        super().__init__()
        if not check_cmd(self.cmd):
            raise OSError(f'Command {self.cmd} not found.')

class GroffExtract:
    def find_sections(self, content, pattern='\.SH'):
        sections = self.find_between(content, pattern)
        return dict([self.split_title(s) for s in sections])

    def subsections(self, content, pattern='\.sp'):
        subsections = self.find_between(pattern, content)
        return dict([self.split_title(s) for s in subsections])

    @staticmethod
    def find_between(content, pattern):
        return re.findall(rf'(?<={pattern})(.*?)(?={pattern}|$)', content, re.DOTALL)

    @staticmethod
    def split_title(content, pattern='\n'):
        content = content.lstrip()
        content = content.replace('\"', '')
        first_split = content.index(pattern)
        title = content[:first_split]
        content = content[first_split:]
        return title.strip(), content.lstrip()

