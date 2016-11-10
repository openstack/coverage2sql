# Copyright 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from oslo_config import cfg
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker

import logging

from coverage2sql.db import models

CONF = cfg.CONF
CONF.register_cli_opt(cfg.BoolOpt('verbose', short='v', default=False,
                                  help='Verbose output including logging of '
                                       'SQL statements'))

DAY_SECONDS = 60 * 60 * 24
Session = None


def setup():
    global engine
    db_uri = make_url(CONF.database.connection)
    # db_backend = db_uri.get_backend_name()

    pool_size = CONF.database.max_pool_size
    pool_recycle = CONF.database.idle_timeout
    if not pool_size and not pool_recycle:
        engine = create_engine(db_uri)
    else:
        engine = create_engine(db_uri,
                               pool_size=pool_size,
                               pool_recycle=pool_recycle)
    global Session
    Session = sessionmaker(bind=engine)


def get_session(autocommit=True, expire_on_commit=False):
    """Get a new sqlalchemy Session instance

    :param bool autocommit: Enable autocommit mode for the session.
    :param bool expire_on_commit: Expire the session on commit defaults False.
    """
    global Session
    if not Session:
        setup()
    session = Session(autocommit=autocommit,
                      expire_on_commit=expire_on_commit)

    # if --verbose was specified, turn on SQL logging
    # note that this is done after the session has been initialized so that
    # we can override the default sqlalchemy logging
    if CONF.get('verbose', False):
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    return session


def create_coverage(project_name, coverage_rate=0.0, report_time=None,
                    test_type='py27', session=None):
    """Create a new coverage record in the database.

    This method is used to add a new coverage in the database.
    It tracks the coverage history.

    :param str project_name: project_name e.g. openstack/tempest
    :param float coverage_rate: coverage_rate defaults to 0
    :param datetime.Datetime report_time: when the coverage was collected
                                          defaults to None
    :param session: optional session object if one isn't provided a new session
                    will be acquired for the duration of this operation
    :return: The coverage object stored in the DB
    :rtype: coverage2sql.models.Coverage
    """
    coverage = models.Coverage()
    coverage.project_name = project_name
    coverage.coverage_rate = coverage_rate
    coverage.test_type = test_type
    if report_time:
        report_time = report_time.replace(tzinfo=None)
        report_time_microsecond = report_time.microsecond
    else:
        report_time_microsecond = None
    coverage.report_time = report_time
    coverage.report_time_microsecond = report_time_microsecond
    session = session or get_session()
    with session.begin():
        session.add(coverage)
    return coverage
