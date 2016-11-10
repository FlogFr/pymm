"""
Pymm Project Tests module
"""
import os
import unittest


class PymmBaseTest(unittest.TestCase):
    """ Base class for all Pymm tests """

    def setUp(self, *args, **kwargs):
        super(PymmBaseTest, self).setUp(*args, **kwargs)
        self.DSN = os.environ['PYMM_DSN']
