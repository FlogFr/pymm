"""
Wrapper around psycopg2.
"""

import psycopg2


conn = None


class Connection(object):
    """ DocString for the class """
    pass


def connect(*args, **kwargs):
    """ Returns the wrapped connection object """
    conn = psycopg2.connect(*args, **kwargs)
    return conn
