===================
Django MySQL Fields
===================

.. image:: https://travis-ci.org/multiplay/django-mysql-fields.png?branch=master
    :target: https://travis-ci.org/multiplay/django-mysql-fields

A small collection of fields which we find useful for using MySQL as our Django database provider.

Requirements
------------

* Python 3.4, 3.5
* Django 1.9.x
* MySQL Community Server 5.6.x
* MySQL Connector Python (Multiplay Fork) - https://github.com/multiplay/mysql-connector-python

Quickstart
----------

1. Install from pypi::

    pip3 install django-mysql-fields

Fields
------

* JSONField - Based on the Django contrib Postgres Field(excluding lookups).
* UUIDField - For storing full UUID's in MySQL.

Running Tests
-------------

1. Download and install Virtualbox and Vagrant.

2. Run Vagrant up installation::

    vagrant up

3. You can then ssh into your newly created Vagrant install::

    vagrant ssh

4. Activate virtualenv from within Vagrant::

    . venv/bin/activate

5. Enter project folder from within Vagrant::

    cd django_mysql_fields

6. Run tests::

    ./test.sh


