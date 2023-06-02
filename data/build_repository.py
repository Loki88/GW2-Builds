#!/usr/bin/env python

import BTrees

from model import Build
from utils import Singleton
from .db import Db


class BuildRepository(metaclass=Singleton):

    def save_build(self, build: Build) -> Build:
        with Db().open_transaction() as connection:
            connection.root.build = build
            return connection.root.build

    def get_build(self) -> Build:
        conn = None
        try:
            conn = Db().open_connection()
            return conn.root.build
        finally:
            if conn is not None:
                conn.close()

    def delete_build(self) -> None:
        with Db().open_transaction() as connection:
            connection.root.build = None
