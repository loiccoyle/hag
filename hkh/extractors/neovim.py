from .sources import Command
from .vim import Vim


class Neovim(Vim):
    required = [Command("nvim")]
    sources = {
        "user": [
            Command(f'nvim -e +"redir>>/dev/stdout | map | redir END" -scq'),
        ]
    }
    has_modes = True
