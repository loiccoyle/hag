import importlib

from ._base import Source


class PythonModule(Source):
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def __bool__(self) -> bool:
        try:
            importlib.import_module(self.module_name)
        except ModuleNotFoundError:
            return False
        return True

    def __repr__(self) -> str:
        return repr(self.module_name)
