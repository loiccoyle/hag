from pathlib import Path
from typing import Union

from ._base import Source


class File(Source):
    def __init__(self, file_path: Union[Path, str]):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.source = file_path

    def fetch(self) -> str:
        with open(self.source, "r") as fp:
            return fp.read()

    def __bool__(self) -> bool:
        return self.source.is_file()

    def __repr__(self) -> str:
        return repr(str(self.source))
