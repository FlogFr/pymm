"""
Foundation module

Contains:
- Pymm is the service class
- SessionBuilder
- Session (from the SessionInterface)
- Client
- ClientPooler
"""


class Pymm(object):
    """ Interface to easily create Session through SessionBuilder"""
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


class Session(object):
    """ Session object in order to query the DB from the client interface """
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
