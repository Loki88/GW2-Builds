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
            except BaseException:
                connection.root.specializations = BTrees.OOBTree.BTree()

    def _save_single_specialization(self, specialization: Specialization, connection):
        connection.root.specializations[specialization.id] = specialization

    def save_specialization(self, specialization: Specialization | list[Specialization]):
        with Db().open_transaction() as connection:
            if (isinstance(specialization, list)):
                for s in specialization:
                    self._save_single_specialization(
                        specialization=s, connection=connection)
            else:
                self._save_single_specialization(
                    specialization=specialization, connection=connection)

    def get_specializations(self, id: int = None, name: str = None) -> list[Specialization]:
        conn = Db().get_connection()
        if (id is None and name is None):
            return list(conn.root.specializations.itervalues())
        elif (id is None):
            return [x for x in conn.root.specializations.itervalues() if x.name == name]
        elif (name is None):
            return conn.root.specializations.get(id, None)
        else:
            spec = conn.root.specializations.get(id, None)
            return spec if spec is not None and spec.name == name else None

    def delete_specializations(self, id: int = None):
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.specializations.clear()
            else:
                connection.root.specializations.pop(id)
