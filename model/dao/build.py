#!/usr/bin/env python

import persistent
import persistent.list
from datetime import datetime


class Build(persistent.Persistent):

    def __init__(self, build_number: int) -> None:
        super().__init__()
        self.build_number = build_number
        self.date = datetime.now()


class BuildManagement(persistent.Persistent):

    def __init__(self) -> None:
        super().__init__()
        self.builds = persistent.list.PersistentList()

    def add_build(self, build: Build) -> None:
        self.builds.append(build)
