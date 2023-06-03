#!/usr/bin/env python

import BTrees

from model import Item, ItemType, BackDetail
from utils import Singleton
from .db import Db


class BackRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.backs is not None:
                    pass
            except BaseException:
                connection.root.backs = BTrees.OOBTree.BTree()

    def _save_single(self, connection, back: Item):
        if (back.type == ItemType.Back):
            connection.root.backs[back.id] = back
            return connection.root.backs[back.id]
        else:
            raise ValueError(back)

    def save_back(self, back: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(back, list)):
                for x in back:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, back)

    def get_back(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.backs.values())
        else:
            return conn.root.backs.get(id, None)

    def delete_back(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.backs.clear()
            else:
                connection.root.backs.pop(id, None)
