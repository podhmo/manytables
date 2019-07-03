import typing as t
import pathlib
from oauth2client.client import OAuth2Credentials
from dictknife.loading._gsuite import get_credentials as get_credentials_from_file
from .configuration import Config


def get_credentials(
    config: Config, *, credentials_path: t.Optional[str] = None, scopes: t.List[str]
) -> OAuth2Credentials:
    credentials_path = pathlib.Path(
        credentials_path or config["credentials"]
    ).expanduser()
    dirpath = pathlib.Path(credentials_path).parent
    if not dirpath.exists():
        dirpath.mkdir(exist_ok=True)

    return get_credentials_from_file(str(credentials_path), scopes=scopes)
