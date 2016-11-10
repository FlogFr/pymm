"""
Testing Pymm Query
"""
from . import PymmBaseTest
from pymm import Where

class QueryTest(PymmBaseTest):
    """ Test all the query objects, chainable and the injection
    inside the query. """

    def test_where_simple_no_arguments(self):
        # test that we can inject a where without arguments
        where = Where('computer_id == 2')
        self.assertEqual(where.query_string, 'computer_id == 2',
                         'Single query should return the query string we pass')
        self.assertEqual(where.arguments, tuple(),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

    def test_where_simple_arguments(self):
        # test that we can inject a where with arguments
        where = Where('name ~* %s', 'laptop')
        self.assertEqual(where.query_string, 'name ~* %s',
                         'Single query should return the query string we pass')
        self.assertEqual(where.arguments, ('laptop', ),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

    def test_where_or(self):
        # test we can chain two simple where condition with a OR boolean
        # condition
        where = Where('name ~* %s', 'laptop').OR(Where('ip == %s', '10.28.123.9'))
        self.assertEqual(where.query_string, '( name ~* %s OR ip == %s )',
                         'The OR operator is not well implemented')
        self.assertEqual(where.arguments, ('laptop', '10.28.123.9'),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

    def test_where_and(self):
        # test we can chain two simple where condition with a AND boolean
        # condition
        where = Where('name ~* %s', 'laptop').AND(Where('ip == %s', '10.28.123.9'))
        self.assertEqual(where.query_string, '( name ~* %s AND ip == %s )',
                         'The AND operator is not well implemented')
        self.assertEqual(where.arguments, ('laptop', '10.28.123.9'),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

    def test_where_chain_included(self):
        # test we can chain inside where in order to make a tree
        where = Where('name ~* %s', 'laptop').AND(
            Where('ip == %s', '10.28.123.9').OR(Where('computer_id in %s', (1, 2, 3)))
        )
        self.assertEqual(where.query_string, '( name ~* %s AND ( ip == %s OR computer_id in %s ) )',
                         'Precedence on the chain of queries boolean logic is not respected')
        self.assertEqual(where.arguments, ('laptop', '10.28.123.9', (1, 2, 3)),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

        where = Where('name ~* %s', 'laptop').OR(
            Where('ip == %s', '10.28.123.9').AND(Where('computer_id in %s', (1, 2, 3)))
        )
        self.assertEqual(where.query_string, '( name ~* %s OR ( ip == %s AND computer_id in %s ) )',
                         'Precedence on the chain of queries boolean logic is not respected')
        self.assertEqual(where.arguments, ('laptop', '10.28.123.9', (1, 2, 3)),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

        where = Where('name ~* %s', 'laptop').OR(
            Where('ip == %s', '10.28.123.9').AND(Where('computer_id in %s', (1, 2, 3)))
        ).AND(
            Where('ip == %s', 'X.X.X.X').AND(Where('computer_id in %s', (1, 2, 3)))
        )
        self.assertEqual(
            where.query_string, '( name ~* %s OR ( ip == %s AND computer_id in %s ) AND ( ip == %s AND computer_id in %s ) )',
            'Precedence on the chain of queries boolean logic is not respected')
        self.assertEqual(where.arguments, ('laptop', '10.28.123.9', (1, 2, 3), 'X.X.X.X', (1, 2, 3)),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')

    def test_where_tree(self):
        # test we have a full possible tree for a where
        where = Where(
            Where(
                'computer_id IN %s', (1, 2, 3, 4, 5)
            ).OR(
                Where('name = %s', 'back1')
            )
        ).AND(
            Where('public = %s', False).OR(
                Where("additional_infos->>'mode' = %s", 'degraded')
            )
        )
        self.assertEqual(
            where.query_string, "( ( computer_id IN %s OR name = %s ) AND ( public = %s OR additional_infos->>'mode' = %s ) )",
            'Where can get where as first arguments to have all precedence possibilities')
        self.assertEqual(where.arguments, ((1, 2, 3, 4, 5), 'back1', False, 'degraded'),
                         'Wrong tuples arguments to be injected in psycopg2 arguments')
