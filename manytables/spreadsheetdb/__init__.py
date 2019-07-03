from __future__ import annotations
import typing as t
import logging
from .. import csvdb  # xxx
from . import auth
from . import access
from .configuration import Config
from .models import Database

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_db(
    config: Config,
    name: str,
    *,
    url: t.Optional[str] = None,
    credentials_path: t.Optional[str] = None,
    scopes: t.List[str] = SCOPES,
) -> Database:
    credentials = auth.get_credentials(
        config, credentials_path=credentials_path, scopes=scopes
    )
    gclient = access.get_client(credentials)
    spreadsheet = access.get_or_create(gclient, name, url=url)
    return Database(spreadsheet, gclient=gclient, url=url)


def save_db(
    config: Config,
    db: csvdb.Database,
    name: str,
    *,
    url: t.Optional[str] = None,
    credentials_path: t.Optional[str] = None,
    scopes: t.List[str] = SCOPES,
) -> MetaData:
    credentials = auth.get_credentials(
        config, credentials_path=credentials_path, scopes=scopes
    )
    gclient = access.get_client(credentials)
    spreadsheet = access.get_or_create(gclient, name, url=url)

    # todo: cleanup
    # todo: sync metadata

    cells = []
    for table in db.tables:
        sheet = access.get_or_create_sheet(spreadsheet, table.name)
        logger.info("create for %r, in %r", sheet, spreadsheet)
        cells.extend(access.to_cells(table.rows))
    logger.info("update cells len=%d, in %r", len(cells), spreadsheet)
    sheet.update_cells(cells, value_input_option="RAW")
    return db.metadata
