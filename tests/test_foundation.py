"""
Testing Foundation

simple run:

pymm = Pymm('pgsql://user:pass@host/first_db') # create a default session
session = pymm['default'] # get the default session

"""
import unittest
import psycopg2


class FoundationTest(unittest.TestCase):
    """ test pymm foundation module """

    def test_simple_connect_and_query_database_with_psycopg2(self):
        """ Simple test the database connectivity """
        conn = psycopg2.connect('dbname=travis_ci_test user=postgres')
        cur = conn.cursor()
        cur.execute('CREATE TABLE test (id integer, value character varying(15));')
        cur.execute("INSERT INTO test (id, value) VALUES (12, 'pouet'), (14, 'ole');")
        cur.execute('SELECT * FROM test;')
        ans = cur.fetchone()
        print('we fetched: {!s}'.format(ans))
        conn.rollback()
        cur.close()
        conn.close()
