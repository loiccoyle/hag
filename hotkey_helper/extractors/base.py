import re
import shlex
import gzip
import subprocess

from shutil import which
from types import GeneratorType
from abc import abstractmethod


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


class CommandFetch:
    def _fetch(self):
        return subprocess.check_output(shlex.split(self.fetch_cmd)).decode('utf8')


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
        if which(self.cmd) is None:
            raise OSError(f'Command {self.cmd} not found.')


class SectionExtract:
    def find_sections(self, content, pattern='\.SH'):
        sections = self.find_between(content, pattern)
        return dict([self.split_title(s) for s in sections])

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

