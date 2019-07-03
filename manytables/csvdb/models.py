from __future__ import annotations
import pathlib
from dictknife import loading
from dictknife.langhelpers import reify
from ..metadata import MetaData


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
        return [Table(fmeta, database=self) for fmeta in self.metadata["db"]["tables"]]

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
        return loading.loadfile(fpath)

    def __iter__(self):
        return iter(self.rows)
