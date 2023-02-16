import json

from ._base import Display


class Text(Display):
    def show(self, modes=None):
        if self.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            hotkeys = {mode: self.hotkeys[mode] for mode in modes}
        else:
            hotkeys = self.hotkeys

        for k, v in hotkeys.items():
            if isinstance(v, dict):
                for key, action in v.items():
                    print(f"{k}: {key}: {action}")
            else:
                print(f"{k}: {v}")


class Json(Display):
    def show(self, modes=None):
        if self.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            hotkeys = {mode: self.hotkeys[mode] for mode in modes}
        else:
            hotkeys = self.hotkeys
        print(json.dumps(hotkeys))
