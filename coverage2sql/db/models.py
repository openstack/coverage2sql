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

import datetime

import sqlalchemy as sa
from sqlalchemy.ext import declarative

BASE = declarative.declarative_base()


class CoverageBase(object):
    """Base class for Coverage Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False

    def save(self, session=None):
        from coverage2sql.db import api as db_api
        super(CoverageBase, self).save(session or db_api.get_session())

    def keys(self):
        return list(self.__dict__.keys())

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def to_dict(self):
        d = self.__dict__.copy()
        d.pop("_sa_instance_state")
        return d


class Coverage(BASE, CoverageBase):
    __tablename__ = 'coverages'
    __table_args__ = (sa.Index('ix_project_name', 'project_name'), )
    id = sa.Column(sa.BigInteger, primary_key=True)
    project_name = sa.Column(sa.String(256),
                             nullable=False)
    coverage_rate = sa.Column(sa.Float())
    test_type = sa.Column(sa.String(256), nullable=False, default='py27')
    report_time = sa.Column(sa.DateTime(), default=datetime.datetime.utcnow())
    report_time_microsecond = sa.Column(sa.Integer(), default=0)


class File(BASE, CoverageBase):
    __tablename__ = 'files'
    __table_args__ = (sa.Index('ix_file_coverage_id', 'coverage_id'),
                      sa.Index('ix_filename', 'filename'))
    id = sa.Column(sa.BigInteger, primary_key=True)
    coverage_id = sa.Column(sa.BigInteger, nullable=False)
    filename = sa.Column(sa.String(256), nullable=False)
    line_rate = sa.Column(sa.Float())
    coverage = sa.orm.relationship(Coverage,
                                   backref=sa.orm.backref('file_coverage'),
                                   foreign_keys=coverage_id,
                                   primaryjoin=coverage_id == Coverage.id)
