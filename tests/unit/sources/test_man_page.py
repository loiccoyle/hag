from unittest import TestCase

from hag.parsers.sources import ManPage


class TestManPage(TestCase):
    def test_check(self):
        source = ManPage("printf")
        assert source

        source = ManPage("somecommandwhichdoesnotexist")
        assert not source

    def test_fetch(self):
        source = ManPage("printf")
        content = source.fetch()
        assert "format and print data" in content
