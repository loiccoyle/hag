from abc import abstractmethod

class Display:
    def __init__(self, ht_dict, has_modes):
        self.ht_dict = ht_dict
        self.has_modes = has_modes

    @abstractmethod
    def show(self, mode=None):
        pass

