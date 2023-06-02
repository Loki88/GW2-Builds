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

    def _save_single(self, connection, rune: Item):
        if (rune.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = rune.details
            if (details.type == UpgradeComponentType.Rune):
                connection.root.runes[rune.id] = rune
                return
        raise ValueError(rune)

    def save_rune(self, rune: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(rune, list)):
                for x in rune:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, rune)

    def get_rune(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.runes.values())
        else:
            return conn.root.runes.get(id, None)

    def delete_rune(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.runes.clear()
            else:
                connection.root.runes.pop(id, None)
