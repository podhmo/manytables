import logging
import pathlib
import qtoml

logger = logging.getLogger(__name__)


def init(debug: bool) -> None:
    filepath = pathlib.Path("manytables.toml")
    if filepath.exists():
        logger.info("%s is already existed", filepath)
        return

    config = {
        "spreadsheet": {
            "credentials": "~/.config/manytables/spreadsheet/creadentials.json"
        }
    }
    with open(filepath, "w") as wf:
        logger.info("create %s, as config file.", filepath)
        qtoml.dump(config, wf)


def clone(source_type: str, url: str, debug: bool) -> None:
    if source_type == "spreadsheet":
        from .spreadsheet import clone

        return clone(url)
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
    sparser.add_argument(
        "--type", dest="source_type", choices=["spreadsheet"], default="spreadsheet"
    )
    sparser.add_argument("--url")

    args = parser.parse_args()
    params = vars(args).copy()
    logging.basicConfig(level=getattr(logging, params.pop("log_level")))
    params.pop("subcommand")(**params)
