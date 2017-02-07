# Copyright (c) 2017 Hewlett Packard Enterprise Development LP
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

"""Add files table

Revision ID: 79dead6f7c26
Revises: cb0e61ce633e
Create Date: 2017-02-07 17:57:28.777311

"""

# revision identifiers, used by Alembic.
revision = '79dead6f7c26'
down_revision = 'cb0e61ce633e'
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

    op.create_table('files',
                    sa.Column('id', id_type, autoincrement=True,
                              primary_key=True),
                    sa.Column('coverage_id', id_type, nullable=False),
                    sa.Column('filename', sa.String(256), nullable=False),
                    sa.Column('line_rate', sa.Float()),
                    mysql_engine='InnoDB')
    op.create_index('ix_class_coverage_id', 'files', ['coverage_id'])
    op.create_index('ix_filename', 'files', ['filename'])


def downgrade():
    op.drop_table('files')
