import argparse
import sys

from . import __version__, displays, extractors


def main():
    parser = argparse.ArgumentParser(description="Extracts and displays hotkeys.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-le",
        "--list-extractors",
        help="list available hotkey extractors.",
        action="store_true",
        dest="list_extractors",
    )
    group.add_argument(
        "-ld",
        "--list-displays",
        help="list available display methods",
        action="store_true",
        dest="list_displays",
    )

    parser.add_argument(
        "extractor",
        nargs="?",
        help="extract hotkey using extractor.",
        choices=[i.lower() for i in extractors.__all__],
    )
    parser.add_argument(
        "-d",
        "--display",
        help="display method.",
        default="Text",
        choices=[i.lower() for i in displays.__all__],
    )
    parser.add_argument(
        "-m", "--modes", help="filter mode", action="append", default=None
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show hkh version and exit."
    )
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    if args.list_displays:
        for i in displays.__all__:
            print(i.lower())
    elif args.list_extractors:
        for i in extractors.__all__:
            try:
                # if the install check passes
                getattr(extractors, i)()
                print(i.lower())
            except OSError:
                pass
    else:
        if args.extractor is None:
            parser.print_help()
            sys.exit(1)
        # get the desired extrator and display
        Extractor = getattr(extractors, args.extractor.title())
        Display = getattr(displays, args.display.title())

        # load hotkeys
        extractor = Extractor()
        fetched = extractor.fetch()
        hotkeys = extractor.extract(fetched)
        # display
        Display(hotkeys, has_modes=extractor.has_modes).show(modes=args.modes)
    # sys.exit(0)


if __name__ == "__main__":
    main()
