import os
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except ModuleNotFoundError:
    print("alacritty config file parsing requires 'pyyaml'.")
    yaml = None

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import Command, File, PythonModule, Web


class Alacritty(Parser):
    required = [Command("alacritty"), PythonModule("pyyaml")]
    sources = {
        "default": [
            Web(
                "https://raw.githubusercontent.com/alacritty/alacritty/master/alacritty.yml"
            )
        ],
        "user": [
            File(
                Path(
                    os.environ.get(
                        "XDG_CONFIG_HOME",
                        Path(os.environ["HOME"]) / ".config",
                    )
                )
                / "alacritty"
                / "alacritty.yml"
            )
        ],
    }
    has_modes = True

    @staticmethod
    def _format_key(bind) -> str:
        if "mods" in bind:
            return f"{bind.get('mods', '').replace('|', '+')}+{bind['key']}"
        else:
            return bind["key"]

    @staticmethod
    def _clean_web(contents: str) -> str:
        keep_line = False
        out = []
        for line in contents.split("\n"):
            if keep_line:
                out.append(line.replace("#-", "-"))
            if line.startswith("#debug"):
                keep_line = False
            if line.startswith("#key_bindings"):
                keep_line = True
                out.append(line.replace("#", ""))
        return "\n".join(out)

    def parse(self, fetched: Dict[str, List[str]]) -> HotkeysWithModes:
        if yaml is None:
            raise ImportError(
                "'pyyaml' is required to parse the alacritty config file."
            )
        out = {}
        for source, contents in fetched.items():
            contents = contents[0]
            if source == "default":
                contents = self._clean_web(contents)
            config_yml = yaml.safe_load(contents)
            for bind in config_yml["key_bindings"]:
                mode = bind.get("mode", "normal")
                if mode not in out:
                    out[mode] = {}
                out[mode][self._format_key(bind)] = bind.get(
                    "action", bind.get("chars")
                )
        return out
