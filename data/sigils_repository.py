#!/usr/bin/env python

import BTrees

from model import Item, UpgradeComponentDetail
from model import ItemType, UpgradeComponentType
from utils import Singleton
from .db import Db


class SigilsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.sigils is not None:
                    pass
            except BaseException:
                connection.root.sigils = BTrees.OOBTree.BTree()

    def _save_single(self, connection, sigil: Item):
        if (sigil.type == ItemType.UpgradeComponent):
            details: UpgradeComponentDetail = sigil.details
            if (details.type == UpgradeComponentType.Sigil):
                connection.root.sigils[sigil.id] = sigil
            return
        raise ValueError(sigil)

    def save_sigil(self, sigil: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(sigil, list)):
                for x in sigil:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, sigil)

    def get_sigil(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.sigils.values())
        else:
            return conn.root.sigils.get(id, None)

    def delete_sigil(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.sigils.clear()
            else:
                connection.root.sigils.pop(id, None)
