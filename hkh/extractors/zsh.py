from .base import Command, Extractor


class Zsh(Extractor):
    required = [Command("zsh")]
    # TODO: this doesn't work for my setup, my config is not sourced :(
    sources = {"user": [Command("zsh -ci bindkey")]}
    has_modes = False

    @staticmethod
    def _clean_key(string):
        string = string.replace('"', "")
        return string

    def extract(self, fetched):
        content = fetched["user"][0]
        out = {}
        for line in content.split("\n"):
            if line:
                key, action = line.split(" ")
                out[self._clean_key(key)] = action
        return out
