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
            module_name, cls_name = model_manager_cls.rsplit('.', 1)
            module = import_module(module_name)
            model_manager_cls = getattr(module, cls_name)
            self.model_manager = model_manager_cls()

    def cursor(self):
        return self.connection.cursor()


class PymmDjango(object):
    """ Pymm Model Manager for Django project """
    pass


__all__ = [
    'Pymm',
    'PymmSession',
    'PymmDjango',
]
