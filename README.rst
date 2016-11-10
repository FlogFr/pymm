.. image:: https://travis-ci.org/aRkadeFR/pymm.svg?branch=master
    :target: https://travis-ci.org/aRkadeFR/pymm

====================================================
Pymm: The Python Object Model Manager for Postgresql
====================================================

`Pymm`_, or `Python`_ Model Manager, is an ORM alternative to doesn't face SQL
performance problem and architecture project while working with PostgresQL.


Philosophy of Pymm
==================

`Pymm`_ is the opposite of an ORM: instead of trying to map programming language
concept in order to create a SQL query, `Pymm`_ give a friendly API to the
developper to create a SQL query, and then map it to `Python`_ object.
If we see SQL as the bottom of the stack, and the language object as the top,
this is a bit the bottom-top philosophy compared to the top to bottom on ORM.
`Pymm` let the full power of the postgres database engine to the developper with
this philosophy in mind.


License
=======

Copyright (C) 2016-current @aRkadeFR

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>


Installation
============

`Pymm`_ is available on PyPi with `pip`_. You can simply install it in your
`Python`_ environment with `pip`_ running the following command line:

```shell
pip install pymm
```

Requirements
============

`Pymm`_ supports `PostgreSQL`_ 9.0+, `Python`_ 2.7, and 3.2+. `Pymm`_ depends of
psycopg2 2.6.0+ to run, it will be automatically installed as a `pip`_ depedency.


Configuration
=============

The minimal configuration of pymm in order to use it is to import the Pymm Model
Manager and instanciate it with the required arguments:

```python
# import Pymm Model Manager in your project.
from pymm import Pymm

# instanciate it with your database settings, you can refer to
# the docstring in order to know all the possible parameter.
pymm = Pymm('dsn'='postgres://user:password@host:port/dbname')
```

You're all set to use `Pymm`_ in your `Django`_, or `Flask`_ project :)



Contribute to Pymm
==================

That's very easy:

* Send feedback on twitter with the #pymm hashtag, or on IRC (freenode - #pymm)
* Report bug on the `bug tracker`_
* Fork and PR
* Sponsor any `Pymm`_ contributor to spread the word in conferences or meetup.
  It's as simple as paying beers and pizza in the different meetup. The
  contributor are available as administrator on IRC (freenode - #pymm)


Unit Tests
==========

To run the full test suite, create a test database, then:
```sh
$ export PYMM_DSN="postgres://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}"
$ python setup.py test
```

To run a specific test:
```sh
$ python -m unittest tests.test_pymm.PymmTest.test_create_default_connection
```


Community support
=================

A freenode channel has been registered in order to talk about `Pymm`_: #pymm


Source code and BugTracker
==========================

If you find any bug or want a feature, a `bug tracker`_ is available on `github
<https://github.com/aRkadeFR/pymm>`_.

You have also the source code on `github repository`_.


History
=======

`Pymm`_ is widely inspired from the concepts of `Pomm`_. After experimenting
database architecture and performance problem in a middle size company, couple
of developpers began to create `Pymm`_, following the philosophy of it.


Thanks
======

Big thanks to @rodoq to continue my SQL and Postgres education and training,
plus making me meet the Pomm author @chanmix
Thank you @chanmix and the `Pomm`_ community for giving me helpful insight
information on `Pomm`_ and SQL.


.. _`Pymm`: https://github.com/aRkadeFR/pymm
.. _`github repository`: https://github.com/aRkadeFR/pymm
.. _`bug tracker`: https://github.com/aRkadeFR/pymm/issues/
.. _`Pomm`: http://www.pomm-project.org/
.. _`Django`: https://www.djangoproject.com/
.. _`PostgreSQL`: http://postgresql.org/
.. _`Python`: https://www.python.org/
.. _`Github`: https://github.com/
