import gzip
import importlib
import shlex
import subprocess
from abc import abstractmethod
from pathlib import Path
from shutil import which
from typing import Union
from urllib import request


# Content sources
class SourceBase:
    @abstractmethod
    def fetch(self) -> str:
        pass

    @abstractmethod
    def check(self) -> bool:
        pass


class PythonModule(SourceBase):
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def check(self) -> bool:
        try:
            importlib.import_module(self.module_name)
        except ModuleNotFoundError:
            return False
        return True

    def __repr__(self) -> str:
        return repr(self.module_name)


class Command(SourceBase):
    def __init__(self, command: str):
        self.source = shlex.split(command)

    def fetch(self) -> str:
        return subprocess.check_output(self.source).decode("utf8")

    def check(self) -> bool:
        return which(self.source[0]) is not None

    def __repr__(self) -> str:
        return repr(" ".join(self.source))


class File(SourceBase):
    def __init__(self, file_path: Union[Path, str]):
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


class Manpage(SourceBase):
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


class Web(SourceBase):
    def __init__(self, url: str):
        self.source = url

    def fetch(self) -> str:
        f = request.urlopen(self.source)
        contents = f.read().decode("utf8")
        return contents

    def check(self) -> bool:
        f = request.urlopen(self.source)
        return f.code == 200

    def __repr__(self) -> str:
        return repr(self.source)
