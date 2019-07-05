import typing as t
import typing_extensions as tx
import logging
import pathlib
from dictknife import loading
from ..metadata import MetaData
from .models import Database

logger = logging.getLogger(__name__)


class Config(tx.TypedDict):
    pass


def load_db(config: Config, dirpath: str) -> Database:
    return Database(pathlib.Path(dirpath))


def get_save_dir(name: str, *, id: t.Optional[str] = None) -> pathlib.Path:
    if id:
        return pathlib.Path(f"{name}-{id}")
    else:
        return pathlib.Path(f"{name}")


def save_db(db, *, name: str = None, with_id: bool = False) -> MetaData:
    name = name or db.name
    dirpath = get_save_dir(db.name, id=db.id if with_id else None)
    dirpath.mkdir(exist_ok=True)

    logger.info("database: %s", dirpath)
    loading.dumpfile(db.metadata, f"{dirpath / 'metadata.toml'}")

    fname_map = {m["name"]: m.get("file") for m in db.metadata["db"]["tables"]}
    for table in db.tables:
        logger.info("table: %s/%s", dirpath, table.name)
        fname = fname_map.get(table.name) or f"{dirpath / table.name}.tsv"

        def gen():
            rows = iter(table)
            try:
                headers = next(rows)
            except StopIteration:
                return

            return (dict(zip(headers, row)) for row in rows)

        loading.dumpfile(gen(), fname)  # tsv ?
    return db.metadata


def save_metadata(metadata: MetaData, dirpath: str):
    dirpath = pathlib.Path(dirpath)
    dirpath.mkdir(exist_ok=True)
    filepath = f"{dirpath / 'metadata.toml'}"
    loading.dumpfile(metadata, filepath)
    logger.info("save metadata: %r", filepath)
