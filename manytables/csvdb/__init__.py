from __future__ import annotations
import typing as t
import typing_extensions as tx
import pathlib
from dictknife import loading
from dictknife.langhelpers import reify


class Config(tx.TypedDict):
    pass


class MetaData(tx.TypedDict):
    url: str
    db: DBMetadata


class DBMetadata(tx.TypedDict):
    id: str
    name: str
    tables: t.List[TableMetadata]


class TableMetadata(tx.TypedDict):
    id: str
    name: str


class Database:
    def __init__(self, dirpath: pathlib.Path):
        self.dirpath = dirpath

    @property
    def id(self):
        return self._metadata["db"]["id"]

    @property
    def name(self):
        return self._metadata["db"]["name"]

    @reify
    def _metadata(self) -> MetaData:
        return MetaData(loading.loadfile(str(self.dirpath / "metadata.toml")))

    @reify
    def tables(self):
        return [Table(fmeta, database=self) for fmeta in self._metadata["db"]["tables"]]

    def __iter__(self):
        return iter(self.tables)


class Table:
    def __init__(self, metadata: dict, *, database: Database) -> None:
        self._metadata = metadata
        self.database = database

    @property
    def id(self):
        return self._metadata["id"]

    @property
    def name(self):
        return self._metadata["name"]

    @reify
    def rows(self):
        fpath = str(self.database.dirpath / f"{self.name}.tsv")
        return loading.loadfile(fpath)

    def __iter__(self):
        return iter(self.rows)


def get_db(config: Config, dirpath: str) -> Database:
    return Database(pathlib.Path(dirpath))
