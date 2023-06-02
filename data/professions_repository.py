#!/usr/bin/env python

import BTrees

from model import Profession
from utils import Singleton
from .db import Db


class ProfessionsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.professions is not None:
                    pass
                else:
                    connection.root.professions = BTrees.OOBTree.BTree()
            except:
                connection.root.professions = BTrees.OOBTree.BTree()

    def _save_single(self, profession: Profession, connection):
        connection.root.professions[profession.id] = profession

    def save_profession(self, profession: Profession | list[Profession]):
        with Db().open_transaction() as connection:
            if (isinstance(profession, list)):
                for p in profession:
                    self._save_single(profession=p, connection=connection)
            else:
                self._save_single(profession=profession, connection=connection)

    def get_professions(self, id: int = None, name: str = None) -> Profession | list[Profession]:
        conn = Db().get_connection()
        if (id is None and name is None):
            return list(conn.root.professions.itervalues())
        elif (id is None):
            return [x for x in conn.root.professions.itervalues() if x.name == name]
        elif (name is None):
            return conn.root.professions.get(id, None)
        else:
            prof = conn.root.professions.get(id, None)
            return prof if prof is not None and prof.name == name else None

    def delete_professions(self, id: int = None):
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.professions.clear()
            else:
                connection.root.professions.pop(id)
