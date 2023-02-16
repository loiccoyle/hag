import gzip
import subprocess
from pathlib import Path

from ._base import Source


class ManPage(Source):
    def __init__(self, page: str):
        self.source = page

    def fetch(self) -> str:
        man_page_path = subprocess.check_output(["man", "-w", self.source]).decode(
            "utf8"
        )
        man_page_path = Path(man_page_path.rstrip())
        with gzip.open(man_page_path, "rb") as gfp:
            return gfp.read().decode("utf8")

    def __bool__(self) -> bool:
        all_pages = (
            subprocess.check_output(["man", "-k", "."]).decode("utf8").split("\n")
        )
        all_pages = [page.split()[0] for page in all_pages if page]
        return self.source in all_pages

    def __repr__(self) -> str:
        return repr(self.source)
