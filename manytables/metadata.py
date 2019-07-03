from __future__ import annotations
import typing as t
import typing_extensions as tx


class MetaData(tx.TypedDict):
    url: str
    resource_type: str  # "spreadsheet" | 
    db: DBMetadata


class DBMetadata(tx.TypedDict):
    id: str
    name: str
    tables: t.List[TableMetadata]


class TableMetadata(tx.TypedDict):
    id: str
    name: str
