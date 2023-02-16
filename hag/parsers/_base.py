import re
from abc import abstractmethod
from typing import Dict, List, Optional, Union

from ..type_specs import Hotkeys, HotkeysWithModes
from .sources import SourceBase


class Parser:
    has_modes: Optional[bool] = None
    sources: Optional[Dict[str, List[SourceBase]]] = None
    required: Optional[List[SourceBase]] = None

    def __init__(self):
        if self.required is not None:
            if not any([source.check() for source in self.required]):
                raise OSError(f"No checks of {self.required} succeeded.")

    def fetch(self) -> Dict[str, List[str]]:
        if self.sources is None:
            raise TypeError("Can't fetch, 'sources' attribute is None.")

        out = {}
        for k, sources in self.sources.items():
            out[k] = [source.fetch() for source in sources if source.check()]
        return out

    @abstractmethod
    def parse(self, fetched: Dict[str, List[str]]) -> Union[Hotkeys, HotkeysWithModes]:
        """Must return a dict with structure:
        if has_modes: {'mode': {'hotkey': 'action'}}
        else: {'hotkey': 'action'}
        """
        pass


class SectionParse:
    """Helper methods to assist in handling man page source documents."""

    def find_sections(self, content: str, pattern: str = r"\.SH"):
        sections = self.find_between(content, pattern)
        return dict([self.split_title(s) for s in sections])

    @staticmethod
    def find_between(content: str, pattern: str):
        return re.findall(rf"(?<={pattern})(.*?)(?={pattern}|$)", content, re.DOTALL)

    @staticmethod
    def split_title(content: str, pattern="\n"):
        content = content.lstrip()
        content = content.replace('"', "")
        first_split = content.index(pattern)
        title = content[:first_split]
        content = content[first_split:]
        return title.strip(), content.lstrip()
