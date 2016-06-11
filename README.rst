.. image:: https://travis-ci.org/aRkadeFR/pymm.svg?branch=master
    :target: https://travis-ci.org/aRkadeFR/pymm

=====
Pymm
=====

``Pymm``, or Python Model Manager, is an ORM alternative to doesn't face SQL
performance problem and architecture project while working with PostgresQL.


License
=======

Copyright (C) 2016 @aRkadeFR

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


How it works
============

``Pymm`` provides two layers in order to query your database and
retrieve objects in Python.

The first layer is the Foundation one, that is a very small wrapper
around psycopg2.

The second layer is the Model Manager. It can be a Model Manager for
Django in order to retrieve your Django model, or a custom one to
retrieve custom objects.

A small example of how it works is:

```python
from pymm import Pymm
pymm = Pymm(default={
                dsn='postgres://user:password@host:port/dbname',
                manager=PymmDjangoManager,
            })

user = pymm.fetchUserById(42)
user # is Django User
```


Installation
============
``Pymm`` and ``PymmDjangoManager`` can be installed by pip with:

```
pip install pymm
```

Then configured in your Django settings:

```
PYMM = {
    'default': {
        'dsn': 'postgres://user:password@host:port/dbname',
        'ModelManager': 'pymm_django.PymmDjangoManager',
    }
}
```

You're all set to use pymm in your Django project :)


Community support
=================

A freenode channel has been registered in order to talk about ``Pymm``: #pymm


Source code and BugTracker
==========================

If you find any bug or want a feature, a bug tracker is available on
`github <https://github.com/aRkadeFR/pymm>`_.

You have also the source code on `github
<https://github.com/aRkadeFR/pymm>`_.


Story
=====

``Pymm`` is widely inspired from the concepts of `Pomm
<http://www.pomm-project.org/>`_.
