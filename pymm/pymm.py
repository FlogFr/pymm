from __future__ import absolute_import

import os
import pkg_resources
import psycopg2
import psycopg2.extras


SETTING_DSN = 'PYMM_DSN'
DEFAULT_DB_ALIAS = 'default'


class Connection(object):
    """
    Connection object store the psycopg2 connection object, along all the data
    about the current database (table list, fields, description)

    The information on the schema are used for the projection of table entity for instance.
    """
    _connection = None
    _information_schema = []

    def __init__(self, connection):
        # init the connection and load all the data in memory
        self._connection = connection

        # load data in memory the information schema
        cursor = connection.cursor()
        fetch_information_schema_path = '/'.join(
            ['sql', 'fetch_information_schema.sql'])
        cursor.execute(pkg_resources.resource_string(__name__, fetch_information_schema_path))
        self._information_schema = cursor.fetchall()
        cursor.close()

    def cursor(self, json=False):
        # return the psycopg2 cursor
        cursor = self._connection.cursor()

        if json:
            kwargs = {
                'conn_or_curs': cursor,
                'globally': False,
                'loads': lambda x: x,
            }
            psycopg2.extras.register_default_json(**kwargs)
            psycopg2.extras.register_default_jsonb(**kwargs)

        return cursor

    def fields(self, table_name):
        return [
            field for field in self._information_schema
            if field[1] == table_name
        ]


class Pymm(object):
    """ Pymm Model Manager, this is the main entry point to pymm features.

    - handle the database sessions
    """
    _instance = None
    _connections = {}

    def __new__(cls, *args, **kwargs):
        # singleton pattern
        if not cls._instance:
            cls._instance = super(Pymm, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, dsn=None):
        dsn = dsn if dsn is not None else os.environ.get(SETTING_DSN, None)
        if dsn is None:
            raise ValueError('Either dsn or the environment variable "{}" is require'.format(SETTING_DSN))

        # store the connection with all data of the database related (table
        # list, fields)
        self._connections[DEFAULT_DB_ALIAS] = Connection(connection=psycopg2.connect(dsn=dsn))

    def __getitem__(self, index):
        """
        Return a psycopg2 connection already instanciated or a new one if it's
        a stale connection.
        """
        return self._connections[index]
