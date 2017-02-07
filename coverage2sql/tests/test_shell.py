# Copyright (c) 2016 Hewlett Packard Enterprise Development L.P.
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

import fixtures
import mock
from oslo_config import cfg
import tempfile

from coverage2sql.migrations import cli as migration_cli
from coverage2sql import shell
from coverage2sql.tests import base


class TestMain(base.TestCase):
    def setUp(self):
        super(TestMain, self).setUp()
        cfg.CONF.reset()
        cfg.CONF.unregister_opt(migration_cli.command_opt)
        self.fake_args = ['coverage2sql', 'test']
        self.useFixture(fixtures.MonkeyPatch('sys.argv', self.fake_args))

    @mock.patch('coverage2sql.read_coverage.ReadCoverage')
    @mock.patch('coverage2sql.shell.process_results')
    def test_main(self, process_results_mock, read_coverage_mock):
        tfile = tempfile.NamedTemporaryFile()
        tfile.write(b'test me later')
        tfile.flush()
        self.fake_args.extend([tfile.name])
        fake_read_coverage = mock.MagicMock('ReadCoverage')
        fake_get_coverage_rate = 'fake coverage rate'
        fake_read_coverage.get_coverage_rate = mock.MagicMock(
            'get_coverage_rate')
        fake_read_coverage.get_coverage_rate.return_value = (
            fake_get_coverage_rate)
        fake_read_coverage.get_rates_by_files = mock.MagicMock(
            'get_rates_by_files')
        fake_read_coverage.get_rates_by_files.return_value = (
            {'filename': 'foo/bar.py', 'line-rate': '0.99'})
        read_coverage_mock.return_value = fake_read_coverage
        shell.main()
        read_coverage_mock.assert_called_with(mock.ANY)
        self.assertEqual(fake_get_coverage_rate,
                         process_results_mock.call_args_list[0][0][1])
