from .base import Display


class Text(Display):
    def show(self, modes=None):
        if self.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            ht_dict = {mode: self.ht_dict[mode] for mode in modes}
        else:
            ht_dict = self.ht_dict

        for k, v in ht_dict.items():
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
            ht_dict = {mode: self.ht_dict[mode] for mode in modes}
        else:
            ht_dict = self.ht_dict
        print(ht_dict)
