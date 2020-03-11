import re
import os
from pathlib import Path

from .base import Extractor
from .base import Command
from .base import File


class Lf(Extractor):
    required = [Command('lf')]
    sources = {'default': [Command('lf -doc')],
               'user': [File(Path(os.environ['XDG_CONFIG_HOME']) / 'lf' / 'lfrc')]}
    has_modes = False

    def _extract(self):
        content_clean = re.compile(r'.*?((boolean)|(string)|(integer)).*\n')
        content_section = re.compile(r'Reference.*?Configuration', re.DOTALL)
        default_key_action = re.compile(r'\s*(.*?)\s*\(default (.*)\)')
        map_key_action = re.compile(r'\s*map\s(\w+)\s*(.*)\n')
        content_clean_quote = re.compile(r'(?<!")\'(?!")')
        # extract the default bindings
        # get the desired section
        content = re.search(content_section, self.fetched['default'][0])[0]
        # clean the problematic lines
        content = re.sub(content_clean, '', content)
        # remove the quotes could be improved
        content = re.sub(content_clean_quote, '', content)
        content = content.replace('\'"\'', '"'). replace('"\'"', '\'')
        out = {}
        for match in re.finditer(default_key_action, content):
            out[match[2]] = match[1]

        for match in re.finditer(map_key_action, content):
            out[match[1]] = match[2]

        # extract the user bindings
        if self.fetched['user']:
            content = self.fetched['user'][0]
            for match in re.finditer(map_key_action, content):
                out[match[1]] = match[2]
        return out
