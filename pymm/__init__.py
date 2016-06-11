"""
 _____   __  __    ___ ___     ___ ___
/\ '__`\/\ \/\ \ /' __` __`\ /' __` __`\
\ \ \L\ \ \ \_\ \/\ \/\ \/\ \/\ \/\ \/\ \
 \ \ ,__/\/`____ \ \_\ \_\ \_\ \_\ \_\ \_\
  \ \ \/  `/___/> \/_/\/_/\/_/\/_/\/_/\/_/
   \ \_\     /\___/
    \/_/     \/__/
"""

"""
Contains:
- Pymm is the service class
- SessionBuilder
- Session (from the SessionInterface)
- Client
- ClientPooler
"""
import abc
import six
import psycopg2
from importlib import import_module


DEFAULT_DB_ALIAS = 'default'


def import_class(full_path):
    module_name, cls_name = full_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, cls_name)


class WrongProjectionException(Exception):
    """ Exception raised when the projection doesn't have the right input
    values """
    pass


class Pymm(object):
    """ Object to easily create connection and interact with the model manager """
    _sessions = {}

    def __init__(self, *args, **kwargs):
        default_dsn = kwargs.pop('dsn', None)
        if default_dsn:
            self._sessions[DEFAULT_DB_ALIAS] = PymmSession(default_dsn)

        for alias, options in kwargs.items():
            self._sessions[alias] = PymmSession(**options)

    def __getitem__(self, index):
        """
        Return a psycopg2 connection already instanciated or a new one if it's
        a stale connection.
        """
        return self._sessions[index]

    @property
    def model_manager(self):
        return self._sessions[DEFAULT_DB_ALIAS].model_manager


class PymmSession(object):
    """ Session object to do the relation between the connection and the
    model manager """
    connection = None
    model_manager = None

    def __init__(self, dsn=None, model_manager_cls=None, **kwargs):
        self.connection = psycopg2.connect(dsn=dsn)
        if model_manager_cls:
            self.model_manager = import_class(model_manager_cls)()

    def cursor(self):
        return self.connection.cursor()

    def projection(self, projection_cls):
        """ construct a new projection object and inject
        this current session into it """
        new_projection = import_class(projection_cls)(self)
        return new_projection


class PymmProjection(object):
    """ default Pymm Model class """
    session = None
    cursor = None
    # this needs to be ordered. PostgresQL does have more performance
    # with clustering data on disk.
    fields = []

    def __init__(self, session):
        self.session = session

    def execute(self, *args, **kwargs):
        if self.cursor:
            self.cursor.closed()

        self.cursor = self.session.cursor()
        self.cursor.execute(*args, **kwargs)
        if list(map(lambda d: d.name, self.cursor.description)) != self.fields:
            raise WrongProjectionException()
        return self

    def fetchone(self):
        return self.cursor.fetchone()


class PymmDjango(object):
    """ Pymm Model Manager for Django project """
    pass


__all__ = [
    'Pymm',
    'PymmSession',
    'PymmDjango',
    'WrongProjectionException',
]
