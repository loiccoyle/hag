<h1 align="center">hag</h1>
<h5 align="center">A Hotkey AGgregator.</h5>
<p align="center">
  <a href="https://pypi.org/project/hag/"><img src="https://img.shields.io/pypi/v/hag"></a>
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img src="https://img.shields.io/badge/platform-linux-informational">
</p>

`hag` is a hotkey aggregator, it tries its best to extract the hotkeys of your software and display them.

It does so by parsing the config files, man pages, command outputs, ... depending on the software.

## Programs

Bellow is a list of implemented software:

<!-- parsers start -->

- Alacritty
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

<!-- parsers end -->

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

<!-- help start -->

```
$ hag -h
usage: hag [-h] [-lp | -ld] [-d {json,text}] [-m MODE] [-v]
           [{alacritty,lf,mpv,neovim,qutebrowser,rofi,sxhkd,sxiv,termite,vim,vimiv,zathura,zsh}]

Hotkey aggregator. All your hotkeys in one place.

positional arguments:
  {alacritty,lf,mpv,neovim,qutebrowser,rofi,sxhkd,sxiv,termite,vim,vimiv,zathura,zsh}
                        Extract hotkeys using parser.

optional arguments:
  -h, --help            show this help message and exit
  -lp, --list-parsers   List available hotkey parsers.
  -ld, --list-displays  List available display methods.
  -d {json,text}, --display {json,text}
                        Display method.
  -m MODE, --modes MODE
                        Filter by mode, if supported by parser.
  -v, --version         Show hag version and exit.
```

<!-- help end -->

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
  hag vim -m Normal -m Visual | rofi -dmenu
  ```
- Use `rofi` to select software and show hotkeys:
  ```sh
  parser="$(hag -le | rofi -dmenu)" && hag "$parser" | rofi -dmenu
  ```

# Contributing

If you want to add support for your favourite software, feel free to open issues/PRs!
