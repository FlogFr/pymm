"""
Foundation module

Contains:
- Pymm is the service class
- SessionBuilder
- Session (from the SessionInterface)
- Client
- ClientPooler
"""
import abc
import six


class Pymm(object):
    """ Object to easily create Session through SessionBuilder """
    _sessions = {}

    def __init__(self, *args, **kwargs):
        """
        Multiple possibility to create Session objects from the
        __init__ of Pymm:

        # create a default session, named default, and created with the
        # default SessionBuilder
        pymm = Pymm('pgsql://user:pass@host/db_name')

        # create named session 'main'
        pymm = Pymm(main='pgsql://user:pass@host/db_name')

        # create named session 'main' with parameter
        pymm = Pymm(main={'dsn': 'pgsql://user:pass@host/db_name', 'param': 'value'})
        """
        pass

    def __getitem__(self, index):
        """
        Return a new session from the SessionBuilder or the cached
        one if already exists
        """
        pass


class SessionInterface(six.with_metaclass(abc.ABCMeta, object)):
    """
    SessionInterface object in order to query the DB from the client interface

    data descriptor with Client in order to communicate between each other

    Is a client.session = Session()
    or session.client = Client() ?

    I think it is client.session = SessionInterface()
    """
    @abc.abstractmethod
    def __get__(self, obj, type=None):
        pass

    @abc.abstractmethod
    def __set__(self, obj, value):
        pass


class Session(SessionInterface):
    """ Session implementation of the SessionInterface """
    def __get__(self, obj, type=None):
        pass

    def __set__(self, obj, value):
        pass


class SessionBuilder(object):
    """ SessionBuilder builds Session objects.  """

    def __init__(self, *args, **kwargs):
        """
        Arguments can be like this:
        session = SB('pgsql://user:pass@host/db_name').session()
        session = SB(dsn='pgsql://user:pass@host/db_name', param='value').session()
        """
        pass

    def session():
        pass


class ClientInterface(object):
    """
    ClientInterface that needs to be implemented by all Clien

    a Session is a data descriptor. This will have a
    """
    session = Session()
