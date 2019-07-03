from __future__ import annotations
import typing as t
import gspread
from dictknife.langhelpers import reify
from ..metadata import MetaData


class Database:
    _gclient: gspread.Client
    _internal: gspread.Spreadsheet

    def __init__(
        self, spreadsheet: gspread.Spreadsheet, *, gclient=gspread.Client, url=None
    ) -> None:
        self._url = url
        self._gclient = gclient
        self._internal = spreadsheet

    @reify
    def metadata(self) -> MetaData:
        url = self._url or f"https://docs.google.com/spreadsheets/d/{self.id}/edit"
        metadata = {
            "url": url,
            "db": {
                "id": self.id,
                "name": self.name,
                "tables": [
                    {"id": table.id, "name": table.name} for table in self.tables
                ],
            },
        }
        return MetaData(metadata)

    @property
    def id(self) -> str:
        return self._internal.id

    @property
    def name(self) -> str:
        return self._internal.title

    @reify
    def tables(self):
        return [Table(ws, database=self) for ws in self._internal.worksheets()]

    def __iter__(self) -> t.Iterable[Table]:
        return iter(self.tables)


class Table:
    database: Database
    _internal: gspread.Worksheet

    def __init__(self, sheet: gspread.Worksheet, *, database: Database):
        self.database = database
        self._internal = sheet

    @property
    def id(self) -> str:
        return self._internal.id

    @property
    def name(self) -> str:
        return self._internal.title

    @property
    def rows(self):
        return self._internal.get_all_values()

    def __iter__(self) -> t.Iterable[dict]:
        return iter(self.rows)
