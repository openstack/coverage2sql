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

import coverage


class DevNull(object):
    """
    A file like '/dev/null'
    """
    def write(self, *args, **kwargs):
        pass


class ReadCoverage(object):

    def __init__(self, coverage_file=None):
        self.cov = coverage.Coverage(data_file=coverage_file)
        self.cov.load()
        self.cov_pct = self.cov.report(file=DevNull())

    def get_data(self):
        return self.cov.get_data()

    def get_coverage_rate(self):
        return self.cov_pct / 100
