<h1 align="center">hag</h1>
<h5 align="center">A Hotkey AGgregator.</h5>
<p align="center">
  <a href="https://pypi.org/project/hag/"><img src="https://img.shields.io/pypi/v/hag"></a>
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img src="https://img.shields.io/badge/platform-linux-informational">
</p>

`hag` is a a hotkey aggregator, it tries its best to extract the hotkeys of your software and display them.

It does so by parsing the config files, man pages, command outputs, ... depending on the software.

## Programs

Bellow is a list of implemented software:

- Lazygit
- Lf
- Mpv
- Neovim
- Qutebrowser
- Rofi
- Sxhkd
- Sxiv
- Termite
- Vim
- Vimiv
- Zathura
- Zsh

## Installation

`hag` is meant to be relatively minimal, as such it doesn't have any dependencies.

```
pip install hag
```

If you just want to use the CLI interface, consider using [`pipx`](https://github.com/pypa/pipx).

```
pipx install hag
```

## Usage

```
$ hag --help
usage: hag [-h] [-le | -ld] [-d {json,text}] [-m MODES] [-v] [{lazygit,lf,mpv,neovim,qutebrowser,rofi,sxhkd,sxiv,termite,vim,vimiv,zathura,zsh}]

Hotkey aggregator. All your hotkeys in one place.

positional arguments:
  {lazygit,lf,mpv,neovim,qutebrowser,rofi,sxhkd,sxiv,termite,vim,vimiv,zathura,zsh}
                        Extract hotkeys using extractor.

options:
  -h, --help            show this help message and exit
  -le, --list-extractors
                        List available hotkey extractors.
  -ld, --list-displays  List available display methods.
  -d {json,text}, --display {json,text}
                        Display method.
  -m MODES, --modes MODES
                        Filter by mode, if supported by extractor.
  -v, --version         Show hag version and exit.
```

### Examples

A few example uses:

- List [`sxhkd`](https://github.com/baskerville/sxhkd) hotkeys:
  ```sh
  hag sxhkd
  ```
- Display `sxhkd` hotkeys in json format and format with [`jq`](https://github.com/stedolan/jq):

  ```sh
  hag sxhkd -d json | jq
  ```

- Show `vim` Normal and Visual mode hotkeys in [`rofi`](https://github.com/davatorium/rofi):
  ```sh
  hag vim -m Normal | rofi -dmenu
  ```
- Use `rofi` to select software and show hotkeys:
  ```sh
  extractor="$(hag -le | rofi -dmenu)" && hag "$extractor" | rofi -dmenu
  ```

# Contributing

If you want to add support for your favourite software, feel free to open issues/PRs!
