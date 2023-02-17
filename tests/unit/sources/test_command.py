from unittest import TestCase

from hag.parsers.sources import Command


class TestCommand(TestCase):
    def test_check(self):
        source = Command("echo some output")
        assert source

        source = Command("somecommandwhichdoesnotexist")
        assert not source

    def test_fetch(self):
        source = Command("echo some output")
        content = source.fetch()
        assert content == "some output\n"
