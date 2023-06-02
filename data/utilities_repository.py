#!/usr/bin/env python

import BTrees

from model import Item, ConsumableDetail
from model import ItemType, ConsumableType
from utils import Singleton
from .db import Db


class UtilitiesRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.utilities is not None:
                    pass
            except:
                connection.root.utilities = BTrees.OOBTree.BTree()

    def _save_single(self, connection, utility: Item) -> Item:
        if (utility.type == ItemType.Consumable):
            details: ConsumableDetail = utility.details
            if (details.type == ConsumableType.Utility):
                connection.root.utilities[utility.id] = utility
                return connection.root.utilities[utility.id]

        connection.rollback()
        raise ValueError(utility)

    def save_utility(self, utility: Item | list[Item]) -> Item | list[Item]:
        with Db().open_transaction() as connection:
            if (isinstance(utility, list)):
                return [self._save_single(connection, x) for x in utility]
            else:
                return self._save_single(connection, utility)

    def get_utility(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.utilities.values())
            else:
                return conn.root.utilities.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_utility(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.utilities.clear()
            else:
                connection.root.utilities.pop(id, None)
