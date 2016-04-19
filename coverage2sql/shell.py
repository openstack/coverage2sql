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
# from oslo_db import options
from pbr import version
from stevedore import enabled

from coverage2sql.db import api
# from coverage2sql import exceptions
# from coverage2sql import read_subunit as subunit

CONF = cfg.CONF
CONF.import_opt('verbose', 'coverage2sql.db.api')

SHELL_OPTS = [
    cfg.MultiStrOpt('coverage_files', positional=True,
                    help='list of coverage files to put into the database'),
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
    # cfg.CONF.register_cli_opts(options.database_opts, group='database')
    cfg.CONF(argv[1:], project='coverage2sql', version=_version_,
             default_config_files=default_config_files)


def process_results(results):
    print(results)


def main():
    cli_opts()

    parse_args(sys.argv)
    if CONF.coverage_files:
        print("From file:")
        process_results("FIXME")  # FIXME
    else:
        print("From stdin:")
        process_results("FIXME")  # FIXME


if __name__ == "__main__":
    sys.exit(main())
