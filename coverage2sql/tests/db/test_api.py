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
