from __future__ import annotations
import logging
import pathlib
from dictknife import loading
from dictknife.langhelpers import reify
from ..metadata import MetaData

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, dirpath: pathlib.Path):
        self.dirpath = dirpath

    @property
    def id(self):
        return self.metadata["db"]["id"]

    @property
    def name(self):
        return self.metadata["db"]["name"]

    @reify
    def metadata(self) -> MetaData:
        return MetaData(loading.loadfile(str(self.dirpath / "metadata.toml")))

    @reify
    def tables(self):
        seen = set()
        tables = []
        for fmeta in self.metadata["db"]["tables"]:
            table = Table(fmeta, database=self)
            seen.add(table.name)
            tables.append(table)
        for fpath in self.dirpath.glob("*.tsv"):
            name = fpath.name[: -len(fpath.suffix)]
            if name in seen:
                continue
            fmeta = {"id": "", "name": name}
            tables.append(Table(fmeta, database=self))
        return tables

    def __iter__(self):
        return iter(self.tables)


class Table:
    def __init__(self, metadata: dict, *, database: Database) -> None:
        self.metadata = metadata
        self.database = database

    @property
    def id(self):
        return self.metadata["id"]

    @property
    def name(self):
        return self.metadata["name"]

    @reify
    def rows(self):
        fpath = str(self.database.dirpath / f"{self.name}.tsv")
        try:
            return loading.loadfile(fpath)
        except FileNotFoundError as e:
            logger.info("%s, %r", fpath, e)
            return []

    def __iter__(self):
        return iter(self.rows)
