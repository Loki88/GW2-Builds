#!/usr/bin/env python

import BTrees

from utils import Singleton
from .db import Db


class PetsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.pets is not None:
                    pass
            except BaseException:
                connection.root.pets = BTrees.OOBTree.BTree()

    # TODO
