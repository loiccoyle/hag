import argparse
import sys

from . import __version__, displays, parsers


def main():
    parser = argparse.ArgumentParser(
        description="Hotkey aggregator. All your hotkeys in one place."
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-lp",
        "--list-parsers",
        help="List available hotkey parsers.",
        action="store_true",
        dest="list_parsers",
    )
    group.add_argument(
        "-ld",
        "--list-displays",
        help="List available display methods.",
        action="store_true",
        dest="list_displays",
    )
    parser.add_argument(
        "parser",
        nargs="?",
        help="Extract hotkeys using parser.",
        choices=[i.lower() for i in parsers.__all__],
    )
    parser.add_argument(
        "-d",
        "--display",
        help="Display method.",
        default="Text",
        choices=[i.lower() for i in displays.__all__],
    )
    parser.add_argument(
        "-m",
        "--modes",
        help="Filter by mode, if supported by parser.",
        action="append",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Show hag version and exit.",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args()

    if args.list_displays:
        for i in displays.__all__:
            print(i.lower())
    elif args.list_parsers:
        for parser in parsers.__all__:
            try:
                # if the install check passes
                getattr(parsers, parser)()
                print(parser.lower())
            except OSError:
                pass
    else:
        if args.parser is None:
            parser.print_help()
            sys.exit(1)
        # get the desired parser and display
        Parser = getattr(parsers, args.parser.title())
        Display = getattr(displays, args.display.title())

        # load hotkeys
        parser = Parser()
        fetched = parser.fetch()
        hotkeys = parser.extract(fetched)
        # display
        Display(hotkeys, has_modes=parser.has_modes).show(modes=args.modes)


if __name__ == "__main__":
    main()
