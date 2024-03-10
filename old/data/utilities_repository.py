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
            except BaseException:
                connection.root.utilities = BTrees.OOBTree.BTree()

    def _save_single(self, connection, utility: Item):
        if (utility.type == ItemType.Consumable):
            details: ConsumableDetail = utility.details
            if (details.type == ConsumableType.Utility):
                connection.root.utilities[utility.id] = utility
            return
        raise ValueError(utility)

    def save_utility(self, utility: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(utility, list)):
                for x in utility:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, utility)

    def get_utility(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.utilities.values())
        else:
            return conn.root.utilities.get(id, None)

    def delete_utility(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.utilities.clear()
            else:
                connection.root.utilities.pop(id, None)
