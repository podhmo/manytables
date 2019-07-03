from __future__ import annotations
import typing as t
import logging
from ..metadata import MetaData
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

    if db.metadata.get("url"):
        if url:
            assert db.metadata["url"] == url
        if name is None:
            url = url or db.metadata["url"]
            logger.info("save_db, update spreadsheet %r, url=%s", name, url)
            spreadsheet = access.get_or_create(gclient, name, url=url)
        else:
            assert db.metadata["db"]["name"] != name
            logger.info("save_db, update spreadsheet %r, url=%s", name, url)
            spreadsheet = access.get_or_create(gclient, name, url=url)
    else:
        logger.info("save_db, create spreadsheet %r", name)
        spreadsheet = gclient.create(name)

    # todo: cleanup

    for table in db.tables:
        cells = access.to_cells(table.rows)
        if not cells:
            continue

        sheet = access.get_or_create_sheet(spreadsheet, table.name)
        logger.info("select %r, in %r", sheet, spreadsheet)
        logger.info("update cells len=%d, in %r", len(cells), spreadsheet)
        sheet.update_cells(cells, value_input_option="RAW")
    return Database(spreadsheet, gclient=gclient, url=url).metadata
