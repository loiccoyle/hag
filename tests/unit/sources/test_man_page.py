from unittest import TestCase

from hag.parsers.sources import ManPage


class TestManPage(TestCase):
    def test_check(self):
        source = ManPage("echo")
        assert source

        source = ManPage("somecommandwhichdoesnotexist")
        assert not source

    def test_fetch(self):
        source = ManPage("echo")
        content = source.fetch()
        assert "echo" in content
