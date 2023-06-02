#!/usr/bin/env python

import BTrees

from model import ItemStats
from utils import Singleton
from .db import Db


class StatsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.stats is not None:
                    pass
            except:
                connection.root.stats = BTrees.OOBTree.BTree()

    def _save_single(self, connection, stat: ItemStats):
        connection.root.stats[stat.id] = stat

    def save_stat(self, stat: ItemStats | list[ItemStats]):
        with Db().open_transaction() as connection:
            if (isinstance(stat, list)):
                for x in stat:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, stat)

    def get_stats(self, id: int = None, name: str = None) -> list[ItemStats]:
        conn = Db().get_connection()
        if (id is None and name is None):
            return list(conn.root.stats.itervalues())
        elif (id is None):
            return [x for x in conn.root.stats.itervalues() if x.name == name]
        elif (name is None):
            return conn.root.stats.get(id, None)
        else:
            stat = conn.root.stats.get(id, None)
            return stat if stat is not None and stat.name == name else None

    def delete_stats(self, id: int = None):
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.stats.clear()
            else:
                connection.root.stats.pop(id)
