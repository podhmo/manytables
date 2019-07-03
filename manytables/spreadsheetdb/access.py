import logging
import gspread
from oauth2client.client import OAuth2Credentials

logger = logging.getLogger(__name__)


def get_client(credentials: OAuth2Credentials) -> gspread.Client:
    return gspread.authorize(credentials)


def get_or_create(gc: gspread.Client, name, url=None, key=None) -> gspread.Spreadsheet:
    if url is not None:
        return gc.open_by_url(url)
    elif key is not None:
        return gc.open_by_key(key)
    else:
        try:
            return gc.open(name)
        except gspread.SpreadsheetNotFound:
            logger.info("spreadsheet %r is not found, creating it", name)
            return gc.create(name)


def get_or_create_sheet(
    wks: gspread.Spreadsheet, name, *, rows=0, cols=0
) -> gspread.Worksheet:
    try:
        return wks.worksheet(name)
    except gspread.WorksheetNotFound:
        logger.info("worksheet %r is not found in %r, creating it", name, wks)
        return wks.add_worksheet(title=name, rows=rows, cols=cols)


def to_cells(rows):
    rows = _iter_rows(rows)
    cells = (
        [gspread.Cell(row=i, col=j, value=v) for j, v in enumerate(row, 1)]
        for i, row in enumerate(rows, 1)
    )
    return [cell for row in cells for cell in row]  # flatten


def _iter_rows(rows):
    itr = iter(rows)
    try:
        first_row = next(itr)
    except StopIteration:
        return

    if hasattr(first_row, "keys"):
        yield list(first_row.keys())
        yield list(first_row.values())
        for row in itr:
            yield list(row.values())
    else:
        yield first_row
        yield from itr
