import unittest


class DumbTest(unittest.TestCase):
    """ DumbTest """

    def test_querying_with_psycopg2(self):
        assert 3 == 3
