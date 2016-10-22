from six import with_metaclass
from .pymm import Pymm, DEFAULT_DB_ALIAS
from .projection import Projection


class Entity(object):
    """ Entity represents a real world object like "student", "employee"

    This is different from the definition of a Model, which is more the
    representation of a database object.
    This tiny difference makes a huge difference on the philosophy the
    developper will use Pymm. """
    projection = Projection()

    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__()


class EntityMeta(type):
    """ MetaClass that will populate the fields for each EntityTable """

    def __init__(cls, cls_name, parents, *args, **kwargs):
        # every time a EntityTable class is created,
        # we need to check and populated all the inside
        # meta information Pymm needs to work with
        if cls_name != 'EntityTable':
            # we don't need
            pymm = Pymm()
            connection = pymm[DEFAULT_DB_ALIAS]
            cls.connection = connection

            if not all(hasattr(cls.Meta, att) for att in ['table', 'schema', 'fields', 'field_pk']):
                raise Exception('''
The Meta class of the Entity "{}" is missing some attributes.
Maybe you forgot the subclass the parent MetaClass like so:
class Meta(EntityTable.Meta):
    pass'''.format(cls))

            if cls.Meta.fields == []:
                # the fields of the entity are not already specify,
                # auto populate them from postgresql
                fields = cls.connection.fields(cls.Meta.table)
                fields.sort(key=lambda x: x[4])
                for field in fields:
                    # append the name of the fields
                    cls.Meta.fields.append(field[0])
                    # check if it's a primary key and add it
                    if field[3]:
                        cls.Meta.field_pk.append(field[0])

            if cls.Meta.fields == []:
                raise Exception('Havent found any fields for the entity {}.'.format(cls))

        super(EntityMeta, cls).__init__(cls_name, parents, *args, **kwargs)


class EntityTable(with_metaclass(EntityMeta, Entity)):
    """ An Entity which is mapping to a database table """
    class Meta:
        # name of the table the entity is mapped to
        table = None
        # optionnal schema the entity is mapped to
        schema = None

        # # # # # # # # # # # # #
        # the following attribute will be populate in the metaclass at the
        # class construction
        #
        # fields of the table
        fields = []
        # fields that are part of the primary key for the table
        field_pk = []

    def __init__(self, *args, **kwargs):
        super(EntityTable, self).__init__(*args, **kwargs)
        projection = kwargs.pop('projection', None)
        if projection:
            for name, value in zip(self.Meta.fields, projection):
                setattr(self, name, value)

    @classmethod
    def findPk(cls, value):
        """ Fetching the entity from the table corresponding to the primary key """
        if cls.Meta.table and cls.Meta.fields:
            template_sql = 'SELECT {} FROM {} WHERE {}'.format(
                ', '.join(cls.Meta.fields),
                cls.Meta.table,
                ''.join('{} = %s'.format(field_pk) for field_pk in cls.Meta.field_pk)
            )
        elif cls.Meta.sql:
            raise NotImplemented('The entity {} doesnt implement findPk method'.format(cls))
        return cls(projection=Projection(template_sql, value)[0])

    @classmethod
    def findAll(cls):
        """ Fetching the entities from the table corresponding to the primary key """
        if cls.Meta.table and cls.Meta.fields:
            template_sql = 'SELECT {} FROM {}'.format(
                ', '.join(cls.Meta.fields), cls.Meta.table
            )
        elif cls.Meta.sql:
            template_sql = cls.Meta.sql
        else:
            raise NotImplemented('The entity {} doesnt implement findAll method'.format(cls))
        return [
            cls(projection=projection)
            for projection in Projection(template_sql, [])
        ]

    @classmethod
    def findWhere(cls, where):
        """ Fetching the entities from the table corresponding to the primary key """
        if cls.Meta.table and cls.Meta.fields:
            template_sql = 'SELECT {} FROM {} WHERE {}'.format(
                ', '.join(cls.Meta.fields),
                cls.Meta.table,
                where.query_string
            )
        elif cls.Meta.sql:
            raise NotImplemented('The entity {} doesnt implement findWhere method'.format(cls))
        return Projection(template_sql, *where.arguments, factory=cls)

    @classmethod
    def countWhere(cls, value):
        """ Counting number of entities where X """
        template_sql = 'SELECT COUNT(*) FROM :table: WHERE :table_pk: = :value:'
        raise NotImplemented()

    @classmethod
    def existWhere(cls, value):
        """ Return True if an entity respecting the where clause exist, otherwise False """
        template_sql = 'SELECT COUNT(*) FROM :table: WHERE :table_pk: = :value:'
        raise NotImplemented()

    @classmethod
    def createAndSave(cls, value):
        """ Create a new record from given data and return an according
        flexible entity. This entity is hydrated with data sent back by the
        database depending on the model’s configured projection so the entity
        has got the default values set by the database. """
        template_sql = 'INSERT INTO :table: VALUES :columns: (:value:) RETURN :columns:'
        raise NotImplemented()

    @classmethod
    def updateOne(cls, value):
        """ Update the given entity and makes it to reflect values changed by
        the database. The fields to be updated are passed as parameter hence
        changed values that are not updated will be override by values in the
        database. This way, the entity reflects what is in the database. """
        template_sql = 'UPDATE :table: VALUES :columns: (:value:) WHERE :pk: RETURN :columns:'
        raise NotImplemented()

    @classmethod
    def deleteOne(cls, value):
        """ Drop an entity and makes it to reflect the last values according to
        the model’s projection. """
        template_sql = 'DELETE FROM :table: WHERE :pk: RETURN :columns:'
        raise NotImplemented()

    @classmethod
    def deleteWhere(cls, value):
        """ Mass deletion, return an iterator on deleted results hydrated by
        the model’s projection. For convenience, it can take a Where instance
        as parameter. """
        template_sql = 'DELETE FROM :table: WHERE :value:'
        raise NotImplemented()
