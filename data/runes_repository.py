#!/usr/bin/env python

import BTrees

from model import Item, UpgradeComponentDetail
from model import ItemType, UpgradeComponentType
from utils import Singleton
from .db import Db


class RunesRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.runes is not None:
                    pass
            except:
                connection.root.runes = BTrees.OOBTree.BTree()

    def _save_single(self, connection, rune: Item) -> Item:
        if (rune.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = rune.details
            if (details.type == UpgradeComponentType.Rune):
                connection.root.runes[rune.id] = rune
                return connection.root.runes[rune.id]

        connection.rollback()
        raise ValueError(rune)

    def save_rune(self, rune: Item | list[Item]) -> Item | list[Item]:
        with Db().open_transaction() as connection:
            if (isinstance(rune, list)):
                return [self._save_single(connection, x) for x in rune]
            else:
                return self._save_single(connection, rune)

    def get_rune(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.runes.values())
            else:
                return conn.root.runes.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_rune(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.runes.clear()
            else:
                connection.root.runes.pop(id, None)
