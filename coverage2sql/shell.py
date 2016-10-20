# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import sys

from oslo_config import cfg
from oslo_db import options
from pbr import version
from stevedore import enabled

from coverage2sql.db import api
# from coverage2sql import exceptions
from coverage2sql import read_coverage as coverage

CONF = cfg.CONF
CONF.import_opt('verbose', 'coverage2sql.db.api')

SHELL_OPTS = [
    cfg.StrOpt('project_name', positional=True, required=True,
                    help='project name of the coverage files'),
    cfg.StrOpt('coverage_file', positional=True,
                    help='A coverage file to put into the database'),
    cfg.StrOpt('connection'),
]

_version_ = version.VersionInfo('coverage2sql').version_string()


def cli_opts():
    for opt in SHELL_OPTS:
        CONF.register_cli_opt(opt)


def list_opts():
    """Return a list of oslo.config options available.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users.
    """
    return [('DEFAULT', copy.deepcopy(SHELL_OPTS))]


def parse_args(argv, default_config_files=None):
    cfg.CONF.register_cli_opts(options.database_opts, group='database')
    cfg.CONF(argv[1:], project='coverage2sql', version=_version_,
             default_config_files=default_config_files)


def process_results(project_name=".", coverage_rate=0.0):
    session = api.get_session()
    api.create_coverage(project_name, coverage_rate)
    session.close()


def main():
    cli_opts()

    parse_args(sys.argv)
    project_name = CONF.project_name
    cov = coverage.ReadCoverage(CONF.coverage_file)
    coverage_rate = cov.get_coverage_rate()
    process_results(project_name, coverage_rate)


if __name__ == "__main__":
    sys.exit(main())
