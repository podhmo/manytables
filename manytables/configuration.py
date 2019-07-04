from __future__ import annotations
import typing as t
import typing_extensions as tx
import logging
import pathlib
from dictknife import loading


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
    return Config(loading.loadfile(str(filepath)))


def dump_init_config(*, path=None) -> None:
    filepath = pathlib.Path(path or DEFAULT_CONFIG_PATH)
    if filepath.exists():
        logger.info("%s is already existed", filepath)
        return

    config = Config(
        {
            "spreadsheet": {
                "credentials": "~/.config/manytables/spreadsheet/credentials.json"
            }
        }
    )
    logger.info("create %s, as config file.", filepath)
    loading.dumpfile(config, str(filepath))
