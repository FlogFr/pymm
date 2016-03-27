=====
Pymm
=====
``Pymm``, or Python Model Manager, is a layer on top of ``psycopg2`` to make SQL and
``Postgres`` features easy within developer's reach.

ORM killer
===========
ORM uses most likely the common subset of features of all the database in order to be
compliant with all of them. This is, by essence, a database feature killer, and ``Pymm``
offers a new way for the developer to interact with the database.

Description
============
``Pymm`` is is a ``Postgres`` access framework. It is intended to have all the power of
``Postgres`` inside Python project.
SQL should be within the developer's reach, to make the most of ``Postgres``. ``Pymm`` is
also a database schema handler.


Objectifs
==========
``Pymm`` has for main objectifs to provides these features:

On the short term:

- control the schema of the database, and easily modify it (big focus on indexes);
- ``Postgresql`` comments for the documentation of the schema;
- easy to write SQL;
- map a projection to a python object;

Leitmotiv
==========
Everything that ``Postgres`` offers should be easily available for the developer.

Story
=====
``Pymm`` is widely inspired from the concepts of `Pomm <http://www.pomm-project.org/>`_.

Thanks @chanmix51 for your work, and all the others present at the PG meetup of Nantes for
the great discussions :)