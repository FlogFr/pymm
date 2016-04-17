"""
Testing Foundation

simple run:

pymm = Pymm('pgsql://user:pass@host/first_db') # create a default session
session = pymm['default'] # get the default session

"""
import os
import unittest
import psycopg2


DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']


class BasicDBTest(unittest.TestCase):
    """ test pymm psycopg2 module """

    def test_simple_connect_and_query_database_with_psycopg2(self):
        """ Simple test the database connectivity """
        conn = psycopg2.connect('dbname={!s} user={!s}'.format(DB_NAME, DB_USER))
        cur = conn.cursor()
        cur.execute('CREATE TABLE test (id integer, value character varying(15));')
        cur.execute("INSERT INTO test (id, value) VALUES (12, 'pouet'), (14, 'ole');")
        cur.execute('SELECT * FROM test;')
        ans = cur.fetchone()
        print('we fetched: {!s}'.format(ans))
        conn.rollback()
        cur.close()
        conn.close()


class FoundationTest(unittest.TestCase):
    """ Test the foundation module """

    def test_dumb(self):
        self.assertEqual(1 + 1, 2)
