import os

from ..type_specs import HotkeysWithModes
from ._base import Parser
from .sources import PythonModule


class Qutebrowser(Parser):
    required = bool(PythonModule("qutebrowser"))
    has_modes = True

    def fetch(self) -> HotkeysWithModes:
        # based on: https://github.com/qutebrowser/qutebrowser/blob/master/qutebrowser/config/configinit.py#L40
        from qutebrowser.config import config, configdata, configfiles  # type: ignore
        from qutebrowser.utils import standarddir  # type: ignore

        standarddir._init_dirs()
        configdata.init()
        yaml_config = configfiles.YamlConfig()
        config.instance = config.Config(yaml_config=yaml_config)
        config.key_instance = config.KeyConfig(config.instance)
        config.val = config.ConfigContainer(config.instance)
        yaml_config.setParent(config.instance)

        config_file = standarddir.config_py()
        if os.path.exists(config_file):
            configfiles.read_config_py(config_file)
        else:
            configfiles.read_autoconfig()

        configfiles.init()
        modes = config.val.bindings.default.keys()
        return {
            mode: {
                str(key): value
                for key, value in config.key_instance.get_bindings_for(mode).items()
            }
            for mode in modes
        }

    def parse(self, fetched: HotkeysWithModes) -> HotkeysWithModes:
        return fetched
