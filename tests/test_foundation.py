"""
Testing Foundation

simple run:

pymm = Pymm('pgsql://user:pass@host/first_db') # create a default session
session = pymm['default'] # get the default session

"""
import os
import unittest
import psycopg2


DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

DSN = 'postgres://{!s}:{!s}@{!s}:{!s}/{!s}'.format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME
)


class BasicDBTest(unittest.TestCase):
    """ test pymm psycopg2 module """

    def test_simple_connect_and_query_database_with_psycopg2(self):
        """ Simple test the database connectivity """
        conn = psycopg2.connect(dsn=DSN)
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE test (id integer, value character varying(15));')
        cur.execute(
            "INSERT INTO test (id, value) VALUES (12, 'pouet'), (14, 'ole');")
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
