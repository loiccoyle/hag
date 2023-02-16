import re
from abc import abstractmethod
from typing import Dict, List, Optional, Union

from ..type_specs import Hotkeys, HotkeysWithModes
from .sources._base import Source


class Parser:
    has_modes: Optional[bool] = None
    sources: Optional[Dict[str, List[Source]]] = None
    required: Optional[bool] = None

    def __init__(self):
        if self.required is not None:
            if not self.required:
                raise OSError(
                    f"Requirements for parsing '{self.__class__.__name__}' not fulfilled."
                )

    def fetch(self) -> Dict[str, List[str]]:
        """Default fetch method. Iterates through the `sources` and calls each source's
        `fetch` method.

        Returns:
            Dictionary of the sources' contents.
        """
        if self.sources is None:
            raise TypeError("Can't fetch, 'sources' attribute is None.")

        out = {}
        for k, sources in self.sources.items():
            out[k] = [source.fetch() for source in sources if source]
        return out

    @abstractmethod
    def parse(self, fetched: Dict[str, List[str]]) -> Union[Hotkeys, HotkeysWithModes]:
        """Parse the fetched sources and generate a Hotkey dictionary.

        Must return a dict with structure:
            if `has_modes`: {'mode': {'hotkey': 'action'}}
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
