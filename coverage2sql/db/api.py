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

import collections
import datetime

from oslo_config import cfg
#from oslo_db.sqlalchemy import session as db_session
import six
import sqlalchemy
from sqlalchemy.engine.url import make_url

import logging

from coverage2sql.db import models
#from coverage2sql import exceptions
#from coverage2sql import read_coverage

CONF = cfg.CONF
CONF.register_cli_opt(cfg.BoolOpt('verbose', short='v', default=False,
                                  help='Verbose output including logging of '
                                       'SQL statements'))

DAY_SECONDS = 60 * 60 * 24

_facades = {}


def _create_facade_lazily():
    global _facades
    db_url = make_url(CONF.database.connection)
    db_backend = db_url.get_backend_name()
    facade = _facades.get(db_backend)
    if facade is None:
        facade = db_session.EngineFacade(
            CONF.database.connection,
            **dict(six.iteritems(CONF.database)))
        _facades[db_backend] = facade
    return facade


def get_session(autocommit=True, expire_on_commit=False):
    """Get a new sqlalchemy Session instance

    :param bool autocommit: Enable autocommit mode for the session.
    :param bool expire_on_commit: Expire the session on commit defaults False.
    """
    facade = _create_facade_lazily()
    session = facade.get_session(autocommit=autocommit,
                                 expire_on_commit=expire_on_commit)

    # if --verbose was specified, turn on SQL logging
    # note that this is done after the session has been initialized so that
    # we can override the default sqlalchemy logging
    if CONF.get('verbose', False):
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    return session
