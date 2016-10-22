==============================
Managing your Database schema
==============================

Web application written in Python should just go on top of an existing database
and not creating the schema. SQL is the best tool to create the schema.

PostgreSQL Schema
=================

PostgreSQL accepts to have `schema`_. Pymm easily maps to any PostgreSQL schema
by providing them in the Meta information of the Entity.


.. _`schema`: https://www.postgresql.org/docs/current/static/ddl-schemas.html
