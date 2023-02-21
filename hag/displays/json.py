import json

from ._base import Display, DisplayText


class Json(DisplayText, Display):
    def format(self, modes=None) -> str:
        hotkeys = self.parse_modes(modes)
        return json.dumps(hotkeys)
