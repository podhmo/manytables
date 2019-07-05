import logging
import sys
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
        from .spreadsheetdb import load_db
        from .csvdb import save_db

        db = load_db(config["spreadsheet"], url=url, name=name)
        save_db(db, name=name, with_id=with_id)
    else:
        print(
            f"invalid source_type {source_type}, not implemented yet?", file=sys.stderr
        )
        sys.exit(1)


def pull(
    *,
    config_path: str,
    source_type: str,
    name: str = None,
    path: str,
    with_id: str,
    debug: bool,
) -> None:
    from .configuration import scan_config
    from .csvdb import load_db as load_db_local
    from .metadata import bind_metadata

    config = scan_config(path=config_path)
    local_db = load_db_local(config, path)
    url = local_db.metadata["url"]

    if source_type == "spreadsheet":
        from .spreadsheetdb import load_db
        from .csvdb import save_db

        db = load_db(config["spreadsheet"], url=url)
        db.metadata = bind_metadata(db.metadata, local_db.metadata)
        save_db(db, with_id=with_id)
    else:
        print(
            f"invalid source_type {source_type}, not implemented yet?", file=sys.stderr
        )
        sys.exit(1)


def show(*, config_path: str, path: str = None, debug: bool, n: int = 5) -> None:
    from .configuration import scan_config
    from .csvdb import load_db

    config = scan_config(path=config_path)
    db = load_db(config, path)
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
    with_id: bool,
    no_save_metadata: bool,
    allow_empty: str,
    debug: bool,
) -> None:
    import pathlib
    from .configuration import scan_config
    from .csvdb import load_db, save_metadata, get_save_dir
    from .metadata import bind_metadata

    config = scan_config(path=config_path)
    name = name or pathlib.Path(path).name

    def _get_db():
        db = load_db(config, path)
        try:
            db.name
        except FileNotFoundError:
            if not allow_empty:
                print(
                    "metadata.toml is not found, if firsttime, please call it with --allow-empty",
                    file=sys.stderr,
                )
                sys.exit(1)
            db.metadata = {"db": {"name": name, "tables": []}}
            db.metadata["db"]["tables"] = [t.metadata for t in db.tables]
        return db

    db = _get_db()
    logger.info("push database: %s", db.name)

    if destination_type == "spreadsheet":
        from .spreadsheetdb import save_db

        metadata = save_db(config["spreadsheet"], db, name=name, url=url)
        metadata = bind_metadata(metadata, db.metadata)

        if no_save_metadata:
            logger.info("no save metadata, skipped")
        elif metadata["db"]["name"] == db.metadata["db"]["name"]:
            save_metadata(metadata, path)
        else:
            save_metadata(
                metadata,
                get_save_dir(
                    metadata["db"]["name"], id=metadata["db"]["id"] if with_id else None
                ),
            )
    else:
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
    sparser.add_argument("--name")
    sparser.add_argument("url")

    # pull
    fn = pull
    sparser = subparsers.add_parser(fn.__name__, description=fn.__doc__)
    sparser.set_defaults(subcommand=fn)
    sparser.add_argument("-c", "--config", dest="config_path", default=None)
    sparser.add_argument("--with-id", action="store_true")
    sparser.add_argument(
        "--type", dest="source_type", choices=["spreadsheet"], default="spreadsheet"
    )
    sparser.add_argument("path")

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
    sparser.add_argument("--with-id", action="store_true")
    sparser.add_argument(
        "--type",
        dest="destination_type",
        choices=["spreadsheet"],
        default="spreadsheet",
    )
    sparser.add_argument("--url")
    sparser.add_argument("--name")
    sparser.add_argument("--allow-empty", action="store_true")
    sparser.add_argument("path")

    args = parser.parse_args()
    params = vars(args).copy()
    logging.basicConfig(level=getattr(logging, params.pop("log_level")))
    params.pop("subcommand")(**params)
