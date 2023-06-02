#!/usr/bin/env python

import BTrees

from model import Build
from utils import Singleton
from .db import Db


class BuildRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.build is not None:
                    pass
            except:
                connection.root.build = None

    def save_build(self, build: Build):
        with Db().open_transaction() as connection:
            connection.root.build = build

    def get_build(self) -> Build:
        conn = Db().get_connection()
        return conn.root.build

    def delete_build(self) -> None:
        with Db().open_transaction() as connection:
            connection.root.build = None
