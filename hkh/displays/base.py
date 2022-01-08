from abc import abstractmethod


class Display:
    def __init__(self, hk_dict, has_modes):
        self.hk_dict = hk_dict
        self.has_modes = has_modes

    @abstractmethod
    def show(self, mode=None):
        pass
