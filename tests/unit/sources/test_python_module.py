from unittest import TestCase

from hag.parsers.sources import PythonModule


class TestPythonModule(TestCase):
    def test_check(self):
        source = PythonModule("hag")
        assert source

        source = PythonModule("somemodulewhichdoesnotexist")
        assert not source

    def test_fetch(self):
        source = PythonModule("hag")
        # No fetch method defined
        content = source.fetch()
        assert content is None
