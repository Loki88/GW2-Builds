#!/usr/bin/env python

class UpgradeItemError(Exception):
    def __init__(self, message):
        super().__init__(message)
