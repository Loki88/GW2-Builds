#!/usr/bin/env python

import BTrees

from model.dao import ItemStats
from utils import Singleton
from .db import Db

class TrinketsRepository(metaclass=Singleton):
        
    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.trinkets is not None:
                    pass
            except:
                connection.root.trinkets = BTrees.OOBTree.BTree()                
    
    
   