from datetime import date

from ._base import Display


class Roff(Display):
    def header(self) -> str:
        parser_name = self.parser.__class__.__name__
        header = f"""\
.TH "{parser_name} Hotkeys" "1" "{date.today()}" "" "hag"
.SH {parser_name} Hotkeys"""
        return header

    def show(self, modes=None):
        if self.parser.has_modes and modes is not None:
            if not (isinstance(modes, list)):
                modes = [modes]
            hotkeys = {mode: self.hotkeys[mode] for mode in modes}
        else:
            hotkeys = self.hotkeys
        print(self.header())

        for k, v in hotkeys.items():
            if isinstance(v, dict):
                print(f".SS {k}")
                for key, action in v.items():
                    print(".TP")
                    print(rf"\fB{key}\fR {action}")
            else:
                print(".TP")
                print(rf"\fB{k}\fR {v}")
