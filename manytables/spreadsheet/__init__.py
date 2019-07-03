from __future__ import annotations
import typing as t
import typing_extensions as tx
import logging
import pathlib
import gspread
from . import auth
from . import access

logger = logging.getLogger(__name__)
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


class Config(tx.TypedDict, total=True):
    credentials: str


class Database:
    _gclient: gspread.Client
    _internal: gspread.Spreadsheet

    def __init__(
        self, spreadsheet: gspread.Spreadsheet, *, gclient=gspread.Client
    ) -> None:
        self._gclient = gclient
        self._internal = spreadsheet

    @property
    def id(self) -> str:
        return self._internal.id

    @property
    def name(self) -> str:
        return self._internal.title

    @property
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


def get_db(
    config: Config,
    name: str,
    *,
    url: t.Optional[str] = None,
    credentials_path: t.Optional[str] = None,
    scopes: t.List[str] = SCOPES,
) -> Database:
    credentials_path = pathlib.Path(
        credentials_path or config["credentials"]
    ).expanduser()
    dirpath = pathlib.Path(credentials_path).parent
    if not dirpath.exists():
        dirpath.mkdir(exist_ok=True)

    credentials = auth.get_credentials(str(credentials_path), scopes=scopes)
    gclient = access.get_client(credentials)

    spreadsheet = access.get_or_create(gclient, name, url=url)
    return Database(spreadsheet, gclient=gclient)
