import logging

logger = logging.getLogger(__name__)


def init(*, debug: bool) -> None:
    from .configuration import dump_init_config

    dump_init_config()


def clone(
    *,
    config_path: str,
    source_type: str,
    name: str = None,
    url: str = None,
    debug: bool,
) -> None:
    from .configuration import scan_config

    config = scan_config(path=config_path)
    if source_type == "spreadsheet":
        from .spreadsheet import get_db

        if name is None:
            assert url
            name = "<unknown>"
        db = get_db(config["spreadsheet"], name=name, url=url)

        print("spreadsheet", db.name)
        for table in db.tables:
            print("sheet", table.name)
            for row in table:
                print(row)
            print("")
    else:
        import sys

        print(
            f"invalid source_type {source_type}, not implemented yet?", file=sys.stderr
        )
        sys.exit(1)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument(
        "--logging",
        choices=list(logging._nameToLevel.keys()),
        default="INFO",
        dest="log_level",
    )
    parser.add_argument("--debug", action="store")

    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    # init
    fn = init
    sparser = subparsers.add_parser(fn.__name__, description=fn.__doc__)
    sparser.set_defaults(subcommand=fn)

    # clone
    fn = clone
    sparser = subparsers.add_parser(fn.__name__, description=fn.__doc__)
    sparser.set_defaults(subcommand=fn)
    sparser.add_argument("-c", "--config", dest="config_path", default=None)
    sparser.add_argument(
        "--type", dest="source_type", choices=["spreadsheet"], default="spreadsheet"
    )
    sparser.add_argument("--url")
    sparser.add_argument("--name")

    args = parser.parse_args()
    params = vars(args).copy()
    logging.basicConfig(level=getattr(logging, params.pop("log_level")))
    params.pop("subcommand")(**params)
