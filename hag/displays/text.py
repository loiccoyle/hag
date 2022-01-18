import json

from ._base import Display


class Text(Display):
    def show(self, modes=None):
        if self.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            hk_dict = {mode: self.hk_dict[mode] for mode in modes}
        else:
            hk_dict = self.hk_dict

        for k, v in hk_dict.items():
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
            hk_dict = {mode: self.hk_dict[mode] for mode in modes}
        else:
            hk_dict = self.hk_dict
        print(json.dumps(hk_dict))
