"""
Testing Pymm Projection
"""
from . import PymmBaseTest
import psycopg2
import mock
from psycopg2 import extras as psy_extras
from pymm import Pymm, Projection, ProjectionJSON


class ProjectionTest(PymmBaseTest):

    def setUp(self, *args, **kwargs):
        super(ProjectionTest, self).setUp(*args, **kwargs)
        self.pymm = Pymm()

    def test_projection(self):
        # projecting a query with pymm should return a Projection instance
        query = "SELECT generate_series(1, %s)"
        params = ('12', )
        args = (query, params)

        projection = Projection(*args)
        self.assertTrue(isinstance(projection, Projection),
                        "Any projections from Pymm Model Manager"
                        "should be a Projection or child instance")

    def test_projection_list(self):
        # a Pymm projection should have the same behavior from psycopg2 execute
        # method, but mapped into a schemaless Projection
        query = "SELECT generate_series(1, %s)"
        params = ('12', )
        args = (query, params)

        projection = Projection(*args)

        # running the same query with psycopg2 in
        # order to retrieve the same thing
        psy_conn = psycopg2.connect(dsn=self.DSN)
        cursor = psy_conn.cursor()
        cursor.execute(*args)

        self.assertEqual(projection.list(), cursor.fetchall(),
                         "The projection list method should be equal "
                         "to the psycopg2 fetchall list")

    def test_projection_iterator_chunk(self):
        # We can use the projection as generator in order
        # to not load all objects into memory at once.
        query = "SELECT generate_series(1, %s)"
        params = ('12', )
        args = (query, params)

        projection = Projection(*args, ITERATOR_CHUNK_SIZE=5)
        psy_conn = psycopg2.connect(dsn=self.DSN)
        cursor = psy_conn.cursor()
        cursor.execute(*args)

        cursor_mock = mock.MagicMock(wraps=cursor)
        with mock.patch.object(projection, '_cursor', new=cursor_mock) as mocked:
            # as there's 12 rows in the projection, the fetchmany should be
            # called three times with an ITERATOR_CHUNK_SIZE=5
            rows = []
            for row in projection:
                rows += row

            self.assertEqual(mocked.fetchmany.call_count, 3,
                             "fetchmany of the cursor object "
                             "should have been called three times")

    def test_projection_json_output(self):
        query = """
SELECT
    ('{\"computer_id\": ' || to_json(computer_id) || ', \"name\": ' || to_json(name) || ', \"additional_infos\": ' || to_json(additional_infos) || '}')::json
FROM
    computer
WHERE
    computer_id = 2
"""
        params = ()
        args = (query, params)

        projection = ProjectionJSON(*args)
        self.assertEqual(projection[0][0], '{"computer_id": 2, "name": "laptop", "additional_infos": {"brand": "thinkpad"}}',
                         "The resulting JSON from the database doesn't match")
