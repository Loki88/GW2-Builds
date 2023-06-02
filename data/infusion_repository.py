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

    def _save_single(self, connection, infusion: Item):
        if (infusion.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = infusion.details
            if (details.type == UpgradeComponentType.Default and InfusionFlag.Infusion in details.infusion_upgrade_flags):
                connection.root.infusions[infusion.id] = infusion
                return
        raise ValueError(infusion)

    def save_infusion(self, infusion: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(infusion, list)):
                for x in infusion:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, infusion)

    def get_infusion(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.infusions.values())
        else:
            return conn.root.infusions.get(id, None)

    def delete_infusion(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.infusions.clear()
            else:
                connection.root.infusions.pop(id, None)
