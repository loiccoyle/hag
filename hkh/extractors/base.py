import re
import shlex
import gzip
import subprocess

from shutil import which
from pathlib import Path
from abc import abstractmethod


class Extractor:
    has_modes = None  # boolean
    sources = None  # dict of sources
    required = None  # None or list of sources at least one of these sources must pass the check

    def __init__(self):
        if self.required is not None:
            if not any([source.check() for source in self.required]):
                raise OSError(f"No checks of {self.required_sources} succeeded.")

    def fetch(self):
        out = {}
        for k, sources in self.sources.items():
            out[k] = [source.fetch() for source in sources if source.check()]
        self.fetched = out
        return self

    @abstractmethod
    def _extract(self):
        """Must return a dict with structure:
       if has_modes: {'mode': {'hotkey': 'action'}}
       else: {'hotkey': 'action'}
        """
        pass

    def extract(self):
        self.extracted = self._extract()
        return self


# Content sources
class Command:
    def __init__(self, command):
        self.source = shlex.split(command)

    def fetch(self):
        return subprocess.check_output(self.source).decode("utf8")

    def check(self):
        return which(self.source[0]) is not None

    def __repr__(self):
        return repr(" ".join(self.source))


class File:
    def __init__(self, file_path):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.source = file_path

    def fetch(self):
        with open(self.source, "r") as fp:
            return fp.read()

    def check(self):
        return self.source.is_file()

    def __repr__(self):
        return repr(str(self.source))


class Manpage:
    def __init__(self, page: str):
        self.source = page

    def fetch(self):
        man_page_path = subprocess.check_output(["man", "-w", self.source]).decode(
            "utf8"
        )
        man_page_path = Path(man_page_path.rstrip())
        with gzip.open(man_page_path, "rb") as gfp:
            return gfp.read().decode("utf8")

    def check(self):
        all_pages = (
            subprocess.check_output(["man", "-k", "."]).decode("utf8").split("\n")
        )
        all_pages = [page.split()[0] for page in all_pages if page]
        return self.source in all_pages

    def __repr__(self):
        return repr(self.source)


# potential sources: url/web


class SectionExtract:
    """Helper methods to assist in handling man page source documents.
    """

    def find_sections(self, content, pattern="\.SH"):
        sections = self.find_between(content, pattern)
        return dict([self.split_title(s) for s in sections])

    @staticmethod
    def find_between(content, pattern):
        return re.findall(rf"(?<={pattern})(.*?)(?={pattern}|$)", content, re.DOTALL)

    @staticmethod
    def split_title(content, pattern="\n"):
        content = content.lstrip()
        content = content.replace('"', "")
        first_split = content.index(pattern)
        title = content[:first_split]
        content = content[first_split:]
        return title.strip(), content.lstrip()
