import typing_extensions as tx


class Config(tx.TypedDict, total=True):
    credentials: str
