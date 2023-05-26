#!/usr/bin/env python

import BTrees

from model.dao import ItemStats
from utils import Singleton
from .db import Db

class UtilitiesRepository(metaclass=Singleton):
        
    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.utilities is not None:
                    pass
            except:
                connection.root.utilities = BTrees.OOBTree.BTree()                
    
    
   