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

"""Add test_type column

Revision ID: cb0e61ce633e
Revises: 52dfb338f74e
Create Date: 2016-10-19 17:48:34.056367

"""

# revision identifiers, used by Alembic.
revision = 'cb0e61ce633e'
down_revision = '52dfb338f74e'
branch_labels = None
depends_on = None

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    op.add_column('coverages', sa.Column('test_type', sa.String(256),
                  nullable=False, server_default='py27'))
    op.create_index('ix_test_type', 'coverages', ['test_type'])


def downgrade():
    op.drop_index('ix_test_type', 'coverages')
    op.drop_column('coverages', 'test_type')
