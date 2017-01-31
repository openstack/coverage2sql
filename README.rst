========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/coverage2sql.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

===============================
coverage2sql README
===============================

Command to Read a coverage file and put the data in a SQL database

coverage2sql is a tool for storing data of test coverage into a SQL database.
With using this tool, you can store time series coverage data and analyze it
if your coverage rate is down.

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/coverage2sql
* Source: http://git.openstack.org/cgit/openstack/coverage2sql
* Bugs: http://bugs.launchpad.net/coverage2sql

Usage
=====

DB Setup
--------

The usage of coverage2sql is split into 2 stages. First you need to prepare a
database with the proper schema; coverage2sql-db-manage should be used to do
this. The utility requires db connection info which can be specified on the
command or with a config file. Obviously the sql connector type, user,
password, address, and database name should be specific to your environment.
coverage2sql-db-manage will use alembic to setup the db schema. You can run the
db migrations with the command::

    coverage2sql-db-manage --database-connection mysql://coverage:pass@127.0.0.1/coverage upgrade head

or with a config file::

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

The only required option is --database-connection. The options can either be
used on the CLI, or put in a config file. If a config file is used you need to
specify the location on the CLI.

TODO
----

To see the TODO, go to the launchpad site:

* `https://bugs.launchpad.net/coverage2sql <https://bugs.launchpad.net/coverage2sql>`_
* `https://blueprints.launchpad.net/coverage2sql <https://blueprints.launchpad.net/coverage2sql>`_

ChangeLog
---------

To see the release notes go here: `http://docs.openstack.org/releasenotes/coverage2sql/ <http://docs.openstack.org/releasenotes/coverage2sql/>`_
