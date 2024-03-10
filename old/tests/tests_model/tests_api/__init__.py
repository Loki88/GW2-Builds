#!/usr/bin/env python

import unittest

from .test_fact import *


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFact)
    return suite
