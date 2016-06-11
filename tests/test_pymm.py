"""
Testing Pymm
"""
import os
import unittest
import psycopg2
import pymm


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


class ComputerProjection(pymm.PymmProjection):
    """ default projection for computer table with all fields """
    fields = ['name', 'ip']


class PymmTest(unittest.TestCase):
    """ Test the foundation module """

    def test_create_default_connection(self):
        my_pymm = pymm.Pymm(dsn=DSN)
        pymm_session = my_pymm['default']
        self.assertIsInstance(pymm_session, pymm.PymmSession)
        cursor = pymm_session.cursor()
        self.assertIsInstance(cursor, psycopg2.extensions.cursor)
        cursor.close()

    def test_create_alias_connection(self):
        my_pymm = pymm.Pymm(primary={'dsn': DSN})
        pymm_session = my_pymm['primary']
        self.assertIsInstance(pymm_session, pymm.PymmSession)
        cursor = pymm_session.cursor()
        self.assertIsInstance(cursor, psycopg2.extensions.cursor)
        cursor.close()

    def test_retrieve_sql_raw(self):
        my_pymm = pymm.Pymm(dsn=DSN)
        cursor = my_pymm['default'].cursor()
        cursor\
            .execute("SELECT name, ip FROM computer WHERE ip = %s;", ('192.168.0.1', ))
        ret = cursor.fetchone()
        self.assertEqual(ret, ('desktop', '192.168.0.1'))
        cursor.close()

    def test_retrieve_raw_projection_one(self):
        my_pymm = pymm.Pymm(dsn=DSN)
        computer = my_pymm['default']\
            .projection('tests.ComputerProjection')\
            .execute("SELECT name, ip FROM computer WHERE ip = %s;", ('192.168.0.1', ))\
            .fetchone()
        self.assertEqual(computer, ('desktop', '192.168.0.1'))

    def test_retrieve_projection_all(self):
        my_pymm = pymm.Pymm(dsn=DSN)
        computer = my_pymm['default']\
            .projection('tests.ComputerProjection')\
            .execute("SELECT name, ip FROM computer WHERE additional_infos IS NULL;")\
            .fetchall()
        self.assertEqual(computer, [('desktop', '192.168.0.1'),
                                    ('front1', '10.28.123.19'),
                                    ('back1', '10.28.123.10'),
                                    ('ci', '192.168.0.8'),
                                    ('back2', '192.168.0.6')])

    def test_retrieve_wrong_projection(self):
        my_pymm = pymm.Pymm(dsn=DSN)
        with self.assertRaises(pymm.WrongProjectionException):
            computer = my_pymm['default']\
                .projection('tests.ComputerProjection')\
                .execute("SELECT computer_id, name, ip FROM computer WHERE ip = %s;", ('192.168.0.1', ))\
                .fetchone()

    def test_retrieve_model_manager(self):
        my_pymm = pymm.Pymm(default={'dsn': DSN,
                                     'model_manager_cls': 'pymm.PymmDjango'})
        model_manager = my_pymm['default'].model_manager
        self.assertIsInstance(model_manager, pymm.PymmDjango)

    def test_retrieve_model_manager_without_alias(self):
        my_pymm = pymm.Pymm(default={'dsn': DSN,
                                     'model_manager_cls': 'pymm.PymmDjango'})
        model_manager = my_pymm.model_manager
        self.assertIsInstance(model_manager, pymm.PymmDjango)
