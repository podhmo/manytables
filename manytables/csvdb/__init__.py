import typing_extensions as tx
import logging
import pathlib
from dictknife import loading
from ..metadata import MetaData
from .models import Database

logger = logging.getLogger(__name__)


class Config(tx.TypedDict):
    pass


def get_db(config: Config, dirpath: str) -> Database:
    return Database(pathlib.Path(dirpath))


def save_db(db, *, with_id: bool = False) -> MetaData:
    if with_id:
        dirpath = pathlib.Path(f"{db.name}-{db.id}")
    else:
        dirpath = pathlib.Path(f"{db.name}")

    dirpath.mkdir(exist_ok=True)
    logger.info("database: %s", dirpath)

    loading.dumpfile(db.metadata, f"{dirpath / 'metadata.toml'}")

    for table in db.tables:
        logger.info("table: %s/%s", dirpath, table.name)
        fname = f"{dirpath / table.name}.tsv"

        def gen():
            rows = iter(table)
            try:
                headers = next(rows)
            except StopIteration:
                return

            return (dict(zip(headers, row)) for row in rows)

        loading.dumpfile(gen(), fname)  # tsv ?
    return db.metadata


def save_metadata(metadata: MetaData, dirpath: str, *, with_id: bool = False):
    dirpath = pathlib.Path(dirpath)
    loading.dumpfile(metadata, f"{dirpath / 'metadata.toml'}")
