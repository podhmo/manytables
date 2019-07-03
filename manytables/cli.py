import logging
from dictknife import loading

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
    with_id: str,
    debug: bool,
) -> None:
    from .configuration import scan_config

    config = scan_config(path=config_path)

    if source_type == "spreadsheet":
        from .spreadsheetdb import get_db
        from .csvdb import save_db

        if name is None:
            assert url
            name = "<unknown>"

        db = get_db(config["spreadsheet"], name=name, url=url)
        save_db(db, with_id=with_id)
    else:
        import sys

        print(
            f"invalid source_type {source_type}, not implemented yet?", file=sys.stderr
        )
        sys.exit(1)


def show(*, config_path: str, path: str = None, debug: bool, n: int = 5) -> None:
    from .configuration import scan_config
    from .csvdb import get_db

    config = scan_config(path=config_path)
    db = get_db(config, path)
    logger.info("database: %s", db.name)
    for table in db.tables:
        logger.info("table: %s", table.name)
        loading.dumpfile(table.rows[:n], format="tsv")
        print("")


def push(
    *,
    config_path: str,
    destination_type: str,
    name: str = None,
    path: str,
    url: str = None,
    no_save_metadata: bool,
    debug: bool,
) -> None:
    from .configuration import scan_config
    from .csvdb import get_db, save_metadata

    config = scan_config(path=config_path)
    db = get_db(config, path)
    logger.info("push database: %s", db.name)

    if destination_type == "spreadsheet":
        from .spreadsheetdb import save_db

        metadata = save_db(config["spreadsheet"], db, name=name, url=url)
        if no_save_metadata:
            logger.info("no save metadata, skipped")
        else:
            save_metadata(metadata, path)
    else:
        import sys

        print(
            f"invalid destination_type {destination_type}, not implemented yet?",
            file=sys.stderr,
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
    sparser.add_argument("--with-id", action="store_true")
    sparser.add_argument(
        "--type", dest="source_type", choices=["spreadsheet"], default="spreadsheet"
    )
    sparser.add_argument("--url")
    sparser.add_argument("--name")

    # show
    fn = show
    sparser = subparsers.add_parser(fn.__name__, description=fn.__doc__)
    sparser.set_defaults(subcommand=fn)
    sparser.add_argument("-c", "--config", dest="config_path", default=None)
    sparser.add_argument("path")

    # push
    fn = push
    sparser = subparsers.add_parser(fn.__name__, description=fn.__doc__)
    sparser.set_defaults(subcommand=fn)
    sparser.add_argument("-c", "--config", dest="config_path", default=None)
    sparser.add_argument("--no-save-metadata", action="store_true")
    sparser.add_argument(
        "--type",
        dest="destination_type",
        choices=["spreadsheet"],
        default="spreadsheet",
    )
    sparser.add_argument("--url")
    sparser.add_argument("--name", required=True)
    sparser.add_argument("path")

    args = parser.parse_args()
    params = vars(args).copy()
    logging.basicConfig(level=getattr(logging, params.pop("log_level")))
    params.pop("subcommand")(**params)
