from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from hag.parsers.sources import File


class TestFile(TestCase):
    @classmethod
    def setUp(cls):
        cls.test_dir = Path("test_file")
        if not cls.test_dir.is_dir():
            cls.test_dir.mkdir()
        cls.test_file = cls.test_dir / "some_file.txt"
        cls.test_file_content = "some content"
        with (cls.test_file).open("w+") as fp:
            fp.write(cls.test_file_content)

    def test_check(self):
        source = File(self.test_file)
        assert source

        source = File(Path("somefilewhichdoesnotexist"))
        assert not source

    def test_fetch(self):
        source = File(self.test_file)
        content = source.fetch()
        assert content == self.test_file_content

    @classmethod
    def tearDown(cls):
        if cls.test_dir.is_dir():
            rmtree(cls.test_dir)
