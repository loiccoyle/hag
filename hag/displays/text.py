from ._base import Display, DisplayText


class Text(DisplayText, Display):
    def format(self, modes=None) -> str:
        hotkeys = self.parse_modes(modes)

        out = []
        for k, v in hotkeys.items():
            if isinstance(v, dict):
                for key, action in v.items():
                    out.append(f"{k}: {key}: {action}")
            else:
                out.append(f"{k}: {v}")
        return "\n".join(out)
