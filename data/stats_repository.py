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

    def _save_single(self, connection, stat: ItemStats) -> ItemStats:
        connection.root.stats[stat.id] = stat
        return connection.root.stats[stat.id]

    def save_stat(self, stat: ItemStats | list[ItemStats]) -> list[ItemStats]:
        with Db().open_transaction() as connection:
            if (isinstance(stat, list)):
                return [self._save_single(connection, x) for x in stat]
            else:
                return self._save_single(connection, stat)

    def get_stats(self) -> list[ItemStats]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.stats.itervalues())
        finally:
            if conn is not None:
                conn.close()

    def get_stat_by_id(self, id: int) -> ItemStats:
        conn = None
        try:
            conn = Db().open_connection()
            return conn.root.stats[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()

    def get_stat_by_name(self, name: str = None) -> list[ItemStats]:
        conn = None
        try:
            conn = Db().open_connection()
            return [x for x in conn.root.stats.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()

    def delete_stats(self):
        with Db().open_transaction() as connection:
            connection.root.stats.clear()

    def delete_stat_by_id(self, id: int):
        with Db().open_transaction() as connection:
            connection.root.stats.pop(id)
