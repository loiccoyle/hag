from typing import Dict, List

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command, PythonModule
from .vim import MODE_MAP


class Neovim(Parser):
    required = all([Command("nvim"), PythonModule("pynvim")])
    has_modes = True

    def fetch(self) -> List[Dict[str, str]]:
        import pynvim

        nvim = pynvim.attach(
            "child", argv=["/bin/env", "nvim", "--embed", "--headless"]
        )
        out = nvim.api.get_keymap("*")
        nvim.quit()
        nvim.close()
        return out

    def parse(self, fetched: List[Dict[str, str]]) -> HotkeysWithModes:
        out = {}
        for map in fetched:
            mode = MODE_MAP[map["mode"]]
            if mode not in out:
                out[mode] = {}
            if map["lhs"].startswith("<Plug>") or not any(
                ["desc" in map, "rhs" in map]
            ):
                continue
            out[mode][map["lhs"].replace(" ", "<space>")] = map.get(
                "desc", map.get("rhs")
            )
        return out
