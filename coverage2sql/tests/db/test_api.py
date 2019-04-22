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

import testscenarios

from coverage2sql.db import api
from coverage2sql.tests import base
from coverage2sql.tests import coverage2sql_fixtures as fixtures
from coverage2sql.tests import db_test_utils

load_tests = testscenarios.load_tests_apply_scenarios


class TestDatabaseAPI(base.TestCase):

    scenarios = [
        ('mysql', {'dialect': 'mysql'}),
        ('postgresql', {'dialect': 'postgres'}),
        ('sqlite', {'dialect': 'sqlite'})
    ]

    def setUp(self):
        super(TestDatabaseAPI, self).setUp()
        self.useFixture(fixtures.LockFixture(self.dialect))
        if not db_test_utils.is_backend_avail(self.dialect):
            raise self.skipTest('%s is not available' % self.dialect)
        if self.dialect == 'mysql':
            self.useFixture(fixtures.MySQLConfFixture())
        elif self.dialect == 'postgres':
            self.useFixture(fixtures.PostgresConfFixture())
        elif self.dialect == 'sqlite':
            self.useFixture(fixtures.SqliteConfFixture())
        self.useFixture(fixtures.Database())

    def test_create_coverage(self):
        cov = api.create_coverage('foo_project')
        self.assertTrue(cov is not None)
        self.assertEqual(cov.project_name, 'foo_project')

    def test_get_coverage_all(self):
        api.create_coverage('foo1_project')
        api.create_coverage('foo2_project')
        covs = api.get_coverage()
        self.assertTrue(covs is not None)
        self.assertEqual(len(covs), 2)
        names = [n.project_name for n in covs]
        self.assertIn(needle='foo1_project', haystack=names)
        self.assertIn(needle='foo2_project', haystack=names)

    def test_get_coverage_with_projenct_name(self):
        api.create_coverage('foo1_project')
        api.create_coverage('foo2_project')
        covs = api.get_coverage(project_name='foo1_project')
        self.assertTrue(covs is not None)
        self.assertEqual(len(covs), 1)
        self.assertEqual(covs[0].project_name, 'foo1_project')

    def test_get_coverage_with_metadata(self):
        api.create_coverage('foo1_project', coverage_metadata="foo,bar")
        api.create_coverage('foo2_project', coverage_metadata="bar,foo")
        covs = api.get_coverage(project_name='foo1_project')
        self.assertTrue(covs is not None)
        self.assertEqual(len(covs), 1)
        self.assertEqual(covs[0].project_name, 'foo1_project')
        self.assertEqual(covs[0].coverage_metadata, 'foo,bar')

    def test_add_file_rates(self):
        rates = []
        rates.append({'filename': 'foo/bar0', 'line-rate': '0'})
        rates.append({'filename': 'foo/bar1', 'line-rate': '1'})
        rates.append({'filename': 'foo/bar2', 'line-rate': '0.92'})
        files = api.add_file_rates(1, rates)
        self.assertEqual(3, len(files))
        for r, f in zip(rates, files):
            self.assertEqual(r['filename'], f.filename)
            self.assertEqual(r['line-rate'], f.line_rate)
