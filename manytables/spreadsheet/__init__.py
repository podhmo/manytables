import typing as t
import typing_extensions as tx
import logging
import pathlib
from . import auth
from . import access

logger = logging.getLogger(__name__)
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


class Config(tx.TypedDict, total=True):
    credentials: str


def clone(
    config: Config,
    name: str,
    *,
    url: t.Optional[str] = None,
    credentials_path: t.Optional[str] = None,
    scopes: t.List[str] = SCOPES,
) -> None:
    credentials_path = pathlib.Path(
        credentials_path or config["credentials"]
    ).expanduser()
    dirpath = pathlib.Path(credentials_path).parent
    if not dirpath.exists():
        dirpath.mkdir(exist_ok=True)

    credentials = auth.get_credentials(str(credentials_path), scopes=scopes)
    gc = access.get_client(credentials)

    wks = access.get_or_create(gc, "manytables", url=url)
    print(f"spreadsheet title: {wks.title}")
    for ws in wks.worksheets():
        print(f"sheet: {ws}")
        for row in ws.get_all_values():
            print(row)
        print("")

    # or
    print(wks.worksheet("Group"))
    print(wks.worksheet("Member"))
    print(wks.worksheet("Member").range("A1:C2"))
