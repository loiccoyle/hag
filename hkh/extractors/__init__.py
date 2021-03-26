from .lazygit import Lazygit
from .lf import Lf
from .mpv import Mpv
from .qutebrowser import Qutebrowser
from .rofi import Rofi
from .sxhkd import Sxhkd
from .sxiv import Sxiv
from .termite import Termite
from .vim import Vim
from .zathura import Zathura
from .zsh import Zsh

__all__ = sorted(
    [
        "Zathura",
        "Sxiv",
        "Rofi",
        "Sxhkd",
        "Qutebrowser",
        "Mpv",
        "Lf",
        "Vim",
        "Termite",
        "Lazygit",
        "Zsh"
    ]
)
