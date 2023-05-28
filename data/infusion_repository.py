#!/usr/bin/env python

import BTrees

from model.dao import Item, UpgradeComponentDetail
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

    def save_infusion(self, infusion: Item):
        if (infusion.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = infusion.details
            if (details.type == UpgradeComponentType.Default and InfusionFlag.Infusion in details.infusion_upgrade_flags):
                with Db().open_transaction() as connection:
                    connection.root.weapons[infusion.id] = infusion
                    return connection.root.weapons[infusion.id]
        raise ValueError(infusion)

    def get_infusion(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.weapons.values())
            else:
                return conn.root.weapons.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_infusion(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.weapons.clear()
            else:
                connection.root.weapons.pop(id, None)
