from __future__ import annotations
import typing as t
import typing_extensions as tx


class MetaData(tx.TypedDict):
    url: str
    resource_type: str  # "spreadsheet" |
    db: DBMetadata


def bind_metadata(self, metadata: MetaData):
    table_map = {t["name"]: t for t in self.get("db", {}).get("tables", [])}
    for table in metadata.get("db", {}).get("tables", []):
        if table["name"] in table_map:
            table_map[table["name"]].update(table)
    return self


class DBMetadata(tx.TypedDict):
    id: str
    name: str
    tables: t.List[TableMetadata]


class TableMetadata(tx.TypedDict):
    id: str
    name: str
