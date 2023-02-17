# from pathlib import Path
# from shutil import rmtree
from unittest import TestCase

from hag.parsers.sources import WebPage


class TestWebPage(TestCase):
    def test_check(self):
        source = WebPage("https://www.someurlwhichdoesnotexist.com")
        assert not source

        source = WebPage("https://example.com")
        assert source

        source = WebPage("http://example.com")
        assert source

    def test_fetch(self):
        source = WebPage("https://example.com")
        content = source.fetch()
        assert "Example Domain" in content
