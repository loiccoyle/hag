from abc import abstractmethod

class Extractor:
    def __init__(self):
        pass

    @abstractmethod
    def _fetch(self):
        '''Must return a string.
        '''
        pass

    def fetch(self):
        self.fetched = self._fetch()
        return self

    @abstractmethod
    def _extract(self):
        '''Must return a dict('hotkey': 'command').
        '''
        pass

    def extract(self):
        self.extracted = self._extract()
        return self

