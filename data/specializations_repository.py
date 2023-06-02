#!/usr/bin/env python

import BTrees

from model import Specialization
from utils import Singleton
from .db import Db


class SpecializationsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.specializations is not None:
                    pass
            except:
                connection.root.specializations = BTrees.OOBTree.BTree()

    def _save_single_specialization(self, specialization: Specialization, connection) -> Specialization:
        connection.root.specializations[specialization.id] = specialization
        return connection.root.specializations[specialization.id]

    def save_specialization(self, specialization: Specialization | list[Specialization]):
        with Db().open_transaction() as connection:
            if (isinstance(specialization, list)):
                return [self._save_single_specialization(specialization=s, connection=connection) for s in specialization]
            else:
                return self._save_single_specialization(specialization=specialization, connection=connection)

    def get_specializations(self, id: int = None, name: str = None) -> list[Specialization]:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None and name is None):
                return list(conn.root.specializations.itervalues())
            elif (id is None):
                return [x for x in conn.root.specializations.itervalues() if x.name is name]
            elif (name is None):
                return conn.root.specializations.get(id, None)
            else:
                spec = conn.root.specializations.get(id, None)
                return spec if spec is not None and spec.name is name else None
        finally:
            if conn is not None:
                conn.close()

    def delete_specializations(self, id: int = None):
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.specializations.clear()
            else:
                connection.root.specializations.pop(id)
