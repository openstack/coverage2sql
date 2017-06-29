=====
Usage
=====

DB Setup
--------

The usage of coverage2sql is split into 2 stages. First you need to prepare a
database with the proper schema; coverage2sql-db-manage should be used to do
this. The utility requires db connection info which can be specified with a
config file. Obviously the sql connector type, user,
password, address, and database name should be specific to your environment.
coverage2sql-db-manage will use alembic to setup the db schema. You can run the
db migrations with a config file::

    coverage2sql-db-manage --config-file etc/coverage2sql.conf upgrade head

This will bring the DB schema up to the latest version for coverage2sql.

.. _coverage2sql:

coverage2sql
------------

Once you have a database setup with the proper database schema you can then use
the coverage2sql command to populate the database with data from your test
coverage file. coverage2sql takes in a `.coverage file`_ through by passing it
file paths as positional arguments to the script at this moment.

.. _.coverage file: http://coverage.readthedocs.io/en/latest/cmd.html#data-file

There are several options for running coverage2sql, they can be listed with::

    coverage2sql --help

The only required option is ``--database-connection``. The options can either be
used on the CLI, or put in a config file. If a config file is used you need to
specify the location on the CLI.

Using in project
----------------

To use coverage2sql in a project::

    import coverage2sql

TODO
----

To see the TODO, go to the launchpad site:

* `https://bugs.launchpad.net/coverage2sql <https://bugs.launchpad.net/coverage2sql>`_
* `https://blueprints.launchpad.net/coverage2sql <https://blueprints.launchpad.net/coverage2sql>`_

ChangeLog
---------

To see the release notes go here: `http://docs.openstack.org/releasenotes/coverage2sql/ <http://docs.openstack.org/releasenotes/coverage2sql/>`_
