#!/usr/bin/env python

import sys
import unittest

import test_loader

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_loader.TestLoader)
    return suite

if __name__ == '__main__':
    unittest.main(sys.modules[__name__])