import subprocess

from .base import Extractor



class zathura(Extractor):
    def __init__(self):
        # check that zatura is installed
        pass

    def _fetch(self):
        return subprocess.check_output(["man", "zathura"])

    def _extract(self):
        return self.fetched

