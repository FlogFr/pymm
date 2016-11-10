======
Entity
======

Entity have these options parametrable in the Meta class:

- database, default to the default one of Pymm
- schema, default to the 'public' schema
- tabe **required**
- fields, if not provided, this will be hydrated automatically from the psycopg2 result, if provided, then it will be only these fields
- sql: this is a custom SQL query
