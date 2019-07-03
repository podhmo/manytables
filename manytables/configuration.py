from __future__ import annotations
import typing as t
import typing_extensions as tx
import logging
import pathlib
import qtoml

logger = logging.getLogger(__name__)
DEFAULT_CONFIG_PATH = "manytables.toml"
if t.TYPE_CHECKING:
    import manytables.spreadsheet


class Config(tx.TypedDict, total=False):
    spreadsheet: "manytables.spreadsheet.Config"


# TODO: typing
def scan_config(*, path=None) -> Config:
    filepath = pathlib.Path(path or DEFAULT_CONFIG_PATH)
    # todo: scan
    with open(filepath) as rf:
        c = Config(qtoml.load(rf))
        return c


def dump_init_config(*, path=None) -> None:
    filepath = pathlib.Path(path or DEFAULT_CONFIG_PATH)
    if filepath.exists():
        logger.info("%s is already existed", filepath)
        return

    config = Config(
        {
            "spreadsheet": {
                "credentials": "~/.config/manytables/spreadsheet/creadentials.json"
            }
        }
    )
    with open(filepath, "w") as wf:
        logger.info("create %s, as config file.", filepath)
        qtoml.dump(config, wf)
