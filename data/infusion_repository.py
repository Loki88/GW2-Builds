#!/usr/bin/env python

import BTrees

from model import Item, UpgradeComponentDetail
from model import ItemType, UpgradeComponentType, InfusionFlag
from utils import Singleton
from .db import Db


class InfusionRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.infusions is not None:
                    pass
            except:
                connection.root.infusions = BTrees.OOBTree.BTree()

    def _save_single(self, connection, infusion: Item) -> Item:
        if (infusion.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = infusion.details
            if (details.type == UpgradeComponentType.Default and InfusionFlag.Infusion in details.infusion_upgrade_flags):
                connection.root.infusions[infusion.id] = infusion
                return connection.root.infusions[infusion.id]

        connection.rollback()
        raise ValueError(infusion)

    def save_infusion(self, infusion: Item | list[Item]) -> Item | list[Item]:
        with Db().open_transaction() as connection:
            if (isinstance(infusion, list)):
                return [self._save_single(connection, x) for x in infusion]
            else:
                return self._save_single(connection, infusion)

    def get_infusion(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.infusions.values())
            else:
                return conn.root.infusions.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_infusion(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.infusions.clear()
            else:
                connection.root.infusions.pop(id, None)
