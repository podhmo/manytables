import typing as t
import logging
import os.path
from oauth2client import file, client
from oauth2client import tools
from oauth2client.client import OAuth2Credentials

logger = logging.getLogger(__name__)

# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/drive.readonly'
#     'https://www.googleapis.com/auth/spreadsheets'
#     'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SCOPE_READONLY = "https://www.googleapis.com/auth/spreadsheets.readonly"


def get_credentials(
    config_path: str,
    *,
    cache_path: t.Optional[str] = None,
    scopes: t.Sequence[str],
    logger: t.Any = logger,
) -> OAuth2Credentials:
    config_path = os.path.expanduser(config_path)
    if cache_path is None:
        cache_path = os.path.join(os.path.dirname(config_path), "token.json")
    cache_path = os.path.expanduser(cache_path)

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    logger.debug("see: %s", cache_path)
    store = file.Storage(cache_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        logger.info("credentials are invalid (or not found). %s", cache_path)
        logger.debug("see: %s", config_path)
        flow = client.flow_from_clientsecrets(config_path, scopes)
        flags = tools.argparser.parse_args(
            ["--logging_level=DEBUG", "--noauth_local_webserver"]
        )
        credentials = tools.run_flow(flow, store, flags=flags)
    return credentials
