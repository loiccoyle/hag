import json

from ._base import Display


class Json(Display):
    def show(self, modes=None):
        if self.parser.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            hotkeys = {mode: self.hotkeys[mode] for mode in modes}
        else:
            hotkeys = self.hotkeys
        print(json.dumps(hotkeys))
