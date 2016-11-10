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

"""Add coverages table

Revision ID: 52dfb338f74e
Revises:
Create Date: 2016-04-19 18:16:52.780046

"""

# revision identifiers, used by Alembic.
revision = '52dfb338f74e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import context
from alembic import op
import sqlalchemy as sa


def upgrade():
    migration_context = context.get_context()
    if migration_context.dialect.name == 'sqlite':
        id_type = sa.Integer
    else:
        id_type = sa.BigInteger

    op.create_table('coverages',
                    sa.Column('id', id_type, autoincrement=True,
                              primary_key=True),
                    sa.Column('project_name', sa.String(256), nullable=False),
                    sa.Column('coverage_rate', sa.Float()),
                    sa.Column('report_time', sa.DateTime()),
                    sa.Column('report_time_microsecond', sa.Integer(),
                              default=0),
                    mysql_engine='InnoDB')
    op.create_index('ix_project_name', 'coverages', ['project_name'])


def downgrade():
    raise NotImplementedError()
