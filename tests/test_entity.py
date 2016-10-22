"""
Testing the Entity feature.
"""
from . import PymmBaseTest
from pymm import Pymm, EntityTable, Where


class ComputerEntity(EntityTable):
    """ Computer docstring that will add
    some specific comment from the database """

    class Meta(EntityTable.Meta):
        table = 'computer'

    def method_test(self):
        return 2


class ComputerEntityCustomField(ComputerEntity):
    class Meta(ComputerEntity.Meta):
        fields = ['name', 'ip', 'additional_infos']


class ComputerManager(EntityTable):
    """ This is a special case of Entity where we
    provide the query to it. By default it takes
    all the fields """
    class Meta(EntityTable.Meta):
        # the fields from * will be expanded
        sql = """
SELECT *
FROM
    computer c
    JOIN manager_computer_m2m mc ON c.computer_id = mc.computer_id
    JOIN manager m ON mc.manager_id = m.user_id
        """


class EntityTest(PymmBaseTest):
    """ test all the entity features """
    def setUp(self):
        super(EntityTest, self).setUp()
        self.pymm = Pymm()

    def test_entity_fields(self):
        # Simple test to find all entities
        self.assertEqual(ComputerEntity.Meta.fields, ['computer_id', 'name', 'ip', 'public', 'additional_infos'],
                         'Introspection of the database got the wrong field for the table computer')

    def test_entity_fields_custom(self):
        # If we have custom fields we should be able to retrieve them
        self.assertEqual(ComputerEntityCustomField.Meta.fields, ['name', 'ip', 'additional_infos'],
                         'Introspection of the database got the wrong field for the table computer')

    def test_entity_find_pk(self):
        # find the entity with the primary key
        computer = ComputerEntity.findPk(2)
        self.assertTrue(isinstance(computer, ComputerEntity),
                        'The instance retrieve is not a Computer')
        self.assertEqual(computer.computer_id, 2,
                         "Didn't retrieve the computer with id 2")

    def test_entity_hydrate_only_fields(self):
        computer = ComputerEntityCustomField.findPk(2)

        self.assertTrue(not hasattr(computer, 'public'),
                        'ComputerEntityCustomField shouldnt have the public field hydrated')

    def test_entity_method(self):
        # find the entity with the primary key
        computer = ComputerEntity.findPk(2)

        # we should be able to call the method of a normal computer
        self.assertEqual(computer.method_test(), 2,
                         'A computer instance should be able to call its methods')

    def test_entity_fetch_all(self):
        # Simple test to find all entities
        computers = ComputerEntity.findAll()
        self.assertEqual(len(computers), 7,
                         "Didn't retrieve the 7 computers from the database")

        computer = computers[0]
        self.assertTrue(isinstance(computer, ComputerEntity),
                        'A computer should be an instance of the ComputerEntity class')
        self.assertEqual(computer.computer_id, 1,
                         'Field computer_id of computer not properly set')
        self.assertEqual(computer.name, 'desktop',
                         'Field name of computer not properly set')
        self.assertEqual(computer.ip, '192.168.0.1',
                         'Field ip of computer not properly set')
        self.assertEqual(computer.public, False,
                         'Field public of computer not properly set')
        self.assertEqual(computer.additional_infos, None,
                         'Field additional_infos of computer not properly set')

    def test_entity_find_where(self):
        # Simple test to find all entities corresponding to the where
        # condition
        #
        # where condition:
        # (computer_id IN (1, 2, 3, 4, 5) OR name = 'back1') AND (public = 'f' OR additional_infos->>'mode' = 'degraded')
        where_cond = Where(
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
        computers = ComputerEntity.findWhere(where_cond)
        self.assertEqual(len(computers.list()), 4,
                         'We should have found 4 computers from the filter condition')

    def test_entity_custom_sql_find_all(self):
        # the ComputerManager is an entity with a custom SQL requests
        computer_managers = ComputerManager.findAll()
        self.assertEqual(len(computer_managers), 8,
                         'The custom SQL query for the entity should return 8 rows')

    def test_entity_custom_sql_find_pk(self):
        # the ComputerManager is an entity with a custom SQL requests which
        # doesn't have a primary key, this should raise an Exception
        with self.assertRaises(Exception):
            ComputerManager.findPk((1,2))

    def test_entity_custom_sql_find_where(self):
        # the ComputerManager is an entity with a custom SQL requests which
        # doesn't have a primary key, this should raise an Exception
        with self.assertRaises(Exception):
            ComputerManager.findWhere(Where('computer_id = 2'))
