from urllib import request
from urllib.error import URLError

from ._base import Source


class WebPage(Source):
    def __init__(self, url: str):
        self.source = url

    def fetch(self) -> str:
        f = request.urlopen(self.source)
        contents = f.read().decode("utf8")
        return contents

    def __bool__(self) -> bool:
        try:
            f = request.urlopen(self.source)
        except URLError:
            return False
        return f.code == 200

    def __repr__(self) -> str:
        return repr(self.source)
