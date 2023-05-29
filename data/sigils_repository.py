#!/usr/bin/env python

import BTrees

from model.dao import Item, UpgradeComponentDetail
from model import ItemType, UpgradeComponentType
from utils import Singleton
from .db import Db


class SigilsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.sigils is not None:
                    pass
            except:
                connection.root.sigils = BTrees.OOBTree.BTree()

    def save_sigil(self, sigil: Item):
        if (sigil.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = sigil.details
            if (details.type == UpgradeComponentType.Sigil):
                with Db().open_transaction() as connection:
                    connection.root.sigils[sigil.id] = sigil
                    return connection.root.sigils[sigil.id]
        raise ValueError(sigil)

    def get_sigil(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.sigils.values())
            else:
                return conn.root.sigils.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_sigil(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.sigils.clear()
            else:
                connection.root.sigils.pop(id, None)
