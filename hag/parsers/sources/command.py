import shlex
import subprocess
from shutil import which

from ._base import Source


class Command(Source):
    def __init__(self, command: str):
        self.source = shlex.split(command)

    def fetch(self) -> str:
        return subprocess.check_output(self.source).decode("utf8")

    def __bool__(self) -> bool:
        return which(self.source[0]) is not None

    def __repr__(self) -> str:
        return repr(" ".join(self.source))
