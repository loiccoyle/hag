from abc import abstractmethod
import gzip
from pathlib import Path
import re
import shlex
from shutil import which
import subprocess
from typing import Dict, List, Optional, Union


class Extractor:
    has_modes: bool = None  # boolean
    sources: Dict[str, List["Source"]] = None  # dict of sources
    required: Optional[
        List["Source"]
    ] = None  # None or list of sources at least one of these sources must pass the check

    def __init__(self):
        if self.required is not None:
            if not any([source.check() for source in self.required]):
                raise OSError(f"No checks of {self.required} succeeded.")

    def fetch(self) -> Dict[str, List[str]]:
        out = {}
        for k, sources in self.sources.items():
            out[k] = [source.fetch() for source in sources if source.check()]
        return out

    @abstractmethod
    def extract(
        self, fetched: Dict[str, List[str]]
    ) -> Dict[str, Union[str, Dict[str, str]]]:
        """Must return a dict with structure:
        if has_modes: {'mode': {'hotkey': 'action'}}
        else: {'hotkey': 'action'}
        """
        pass


# Content sources
class Source:
    @abstractmethod
    def fetch(self) -> str:
        pass

    @abstractmethod
    def check(self) -> bool:
        pass


class Command(Source):
    def __init__(self, command):
        self.source = shlex.split(command)

    def fetch(self) -> str:
        return subprocess.check_output(self.source).decode("utf8")

    def check(self) -> bool:
        return which(self.source[0]) is not None

    def __repr__(self) -> str:
        return repr(" ".join(self.source))


class File(Source):
    def __init__(self, file_path):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.source = file_path

    def fetch(self) -> str:
        with open(self.source, "r") as fp:
            return fp.read()

    def check(self) -> bool:
        return self.source.is_file()

    def __repr__(self) -> str:
        return repr(str(self.source))


class Manpage(Source):
    def __init__(self, page: str):
        self.source = page

    def fetch(self) -> str:
        man_page_path = subprocess.check_output(["man", "-w", self.source]).decode(
            "utf8"
        )
        man_page_path = Path(man_page_path.rstrip())
        with gzip.open(man_page_path, "rb") as gfp:
            return gfp.read().decode("utf8")

    def check(self) -> bool:
        all_pages = (
            subprocess.check_output(["man", "-k", "."]).decode("utf8").split("\n")
        )
        all_pages = [page.split()[0] for page in all_pages if page]
        return self.source in all_pages

    def __repr__(self) -> str:
        return repr(self.source)


# potential sources: url/web


class SectionExtract:
    """Helper methods to assist in handling man page source documents."""

    def find_sections(self, content, pattern=r"\.SH"):
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
