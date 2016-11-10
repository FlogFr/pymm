from __future__ import absolute_import

from future.utils import implements_iterator

from .pymm import Pymm, DEFAULT_DB_ALIAS
from .query import Where


DEFAULT_ITERATOR_CHUNK_SIZE = 1000


@implements_iterator
class Projection(object):
    """ Projection makes a SQL query and stores its result.

    This is by definition schemaless. This is the main
    point of the interface with psycopg2 for Entity. """
    _cursor = None
    _list = None
    _sql = None
    _args = []

    def __init__(self, SQL_QUERY=None, *args, **kwargs):
        self._sql = SQL_QUERY
        self._args = args

        # variable to have full feature on iterator
        self._iterator_finished = False
        self._iterator_chunk_size = kwargs.pop('ITERATOR_CHUNK_SIZE', DEFAULT_ITERATOR_CHUNK_SIZE)
        self._current_chunk = []

        # additional query
        self._where = []

    def __iter__(self):
        return self

    def _create_cursor(self):
        """ This methods creates the cursor """
        self._cursor = Pymm()[DEFAULT_DB_ALIAS].cursor()

    def __next__(self):
        """ Iter on the PG cursor in order to retrieve the list.

        This is an iterator and iters by chunk of ITERATOR_CHUNK_SIZE rows. """
        if not self._cursor:
            self._create_cursor()
            self._cursor.execute(self._sql, self._args)

        if not self._current_chunk and not self._iterator_finished:
            # we don't have any more result in the current chunk, and we are
            # not at the end of the cursor
            self._current_chunk = self._cursor.fetchmany(self._iterator_chunk_size)
            if len(self._current_chunk) < self._iterator_chunk_size:
                # we have less than the chunk size we requested,
                # meaning we have finished iterating the cursor
                self._iterator_finished = True
            else:
                self._iterator_finished = False

        if self._current_chunk:
            # we have a current list of result, we need to return it
            # row per row
            return self._current_chunk.pop(0)
        else:
            # we don't have anymore results to be returned
            self._cursor.close()
            raise StopIteration()

    def __getitem__(self, index):
        """
        Return a psycopg2 connection already instanciated or a new one if it's
        a stale connection.
        """
        return self.list()[index]

    def list(self):
        if self._list is None:
            self._list = list(self)

        return self._list

    def where(self, *args, **kwargs):
        # add a where on the query
        self._where.append(Where(*args, **kwargs))


class ProjectionJSON(Projection):
    """ This projection will result as a string for each row and with
    performance improvement cause the JSON is generated on the DB size and not
    casting twice while fetching the values. This is greatly appreciated in API
    when you have simple data to directly be returned from the DB."""

    def _create_cursor(self):
        """ This methods creates the cursor and set
        the noop on the json cast from psycopg2.
        http://initd.org/psycopg/docs/extras.html#json-adaptation """
        self._cursor = Pymm()[DEFAULT_DB_ALIAS].cursor(json=True)
        pass
