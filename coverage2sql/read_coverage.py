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

import tempfile

import coverage
import xmltodict


class DevNull(object):
    """A file like '/dev/null' """
    def write(self, *args, **kwargs):
        pass


class ReadCoverage(object):

    def __init__(self, coverage_file=None):
        self.cov = coverage.Coverage(data_file=coverage_file)
        self.cov.load()
        xmlfile = tempfile.NamedTemporaryFile(suffix='.xml')
        self.cov_pct = self.cov.xml_report(outfile=xmlfile.name)
        self.covdoc = xmltodict.parse(xmlfile.read())
        xmlfile.close()

    def get_data(self):
        return self.cov.get_data()

    def get_coverage_rate(self):
        return self.cov_pct / 100

    def get_rates_by_files(self):
        rates = []
        for p in self.covdoc['coverage']['packages']['package']:
            try:
                # FIXME(masayukig): Try to access the first element. This is
                # ugly..
                p['classes']['class'][0]
                for c in p['classes']['class']:
                    rates.append({'filename': c['@filename'],
                                  'line-rate': c['@line-rate']})
            except KeyError:
                # NOTE(masayukig): This has only one class
                c = p['classes']['class']
                rates.append({'filename': c['@filename'],
                              'line-rate': c['@line-rate']})
        return rates
