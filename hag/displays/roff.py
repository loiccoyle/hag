from datetime import date

from ._base import Display, DisplayText


class Roff(DisplayText, Display):
    def header(self) -> str:
        parser_name = self.parser.__class__.__name__
        header = f"""\
.TH "{parser_name} Hotkeys" "1" "{date.today()}" "" "hag"
.SH {parser_name} Hotkeys"""
        return header

    def format(self, modes=None) -> str:
        hotkeys = self.parse_modes(modes)
        out = [self.header()]

        for k, v in hotkeys.items():
            if isinstance(v, dict):
                out.append(f".SS {k}")
                for key, action in v.items():
                    out.append(".TP")
                    out.append(rf"\fB{key}\fR {action}")
            else:
                out.append(".TP")
                out.append(rf"\fB{k}\fR {v}")
        return "\n".join(out)
