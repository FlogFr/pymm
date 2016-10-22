"""
Testing Pymm
"""
from . import PymmBaseTest
import psycopg2

from pymm import Pymm, Connection, DEFAULT_DB_ALIAS


class BasicDBTest(PymmBaseTest):
    """ test pymm psycopg2 module """

    def test_simple_connect_and_query_database_with_psycopg2(self):
        # Simple test the database connectivity
        conn = psycopg2.connect(dsn=self.DSN)
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE test (id integer, value character varying(15));')
        cur.execute(
            "INSERT INTO test (id, value) VALUES (12, 'pouet'), (14, 'ole');")
        cur.execute('SELECT * FROM test;')
        ans = cur.fetchone()
        conn.rollback()
        cur.close()
        conn.close()


class PymmTest(PymmBaseTest):
    """ Test Pymm Model Manager entry point """

    def test_create_default_connection(self):
        # create a psycopg2 connection and retrieve it
        from psycopg2.extensions import connection

        pymm = Pymm()
        pymm_connection = pymm['default']
        self.assertTrue(isinstance(pymm_connection, Connection),
                         "The pymm connection isn't a psycopg2 connection")

        # test the connection is OK
        cursor = pymm_connection.cursor()
        cursor.execute("SELECT (1);")
        sql_ret = cursor.fetchone()
        self.assertEqual(sql_ret, (1, ),
                         "We didn't retrieve the simple row from postgres")

    def test_store_information_schema(self):
        # At the load of any connection to the database,
        # the connection is stored and save along all the information of
        # the database of the connection: table list, fields list of tables,
        # the description of fields
        pymm = Pymm()

        self.assertEqual(len([t for t in pymm._connections[DEFAULT_DB_ALIAS]._information_schema
                              if t[1] == 'computer']), 5,
                         "The table computer contains 5 fields and should only have 5 row in the information_schema")
        # columns are as follow:
        # column_name, table_name, table_schema, column_pk, ordinal_position, is_nullable, description
        self.assertTrue(('computer_id', 'computer', 'public', True, 1, False, None)
                        in pymm._connections[DEFAULT_DB_ALIAS]._information_schema,
                        'Information of the "computer" table should be present in the information_schema')
        self.assertTrue(('ip', 'computer', 'public', False, 3, False, 'Public network IP of the Computer')
                        in pymm._connections[DEFAULT_DB_ALIAS]._information_schema,
                        'Information of the "computer" table should be present in the information_schema')
        self.assertTrue(('additional_infos', 'computer', 'public', False, 5, True, None)
                        in pymm._connections[DEFAULT_DB_ALIAS]._information_schema,
                        'Information of the "computer" table should be present in the information_schema')
