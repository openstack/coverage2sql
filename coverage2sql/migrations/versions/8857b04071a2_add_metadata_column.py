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

"""Add metadata column

Revision ID: 8857b04071a2
Revises: 79dead6f7c26
Create Date: 2019-04-18 12:12:34.776240

"""

# revision identifiers, used by Alembic.
revision = '8857b04071a2'
down_revision = '79dead6f7c26'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('coverages', sa.Column('coverage_metadata', sa.String(256),
                  nullable=True))
    op.create_index('ix_coverage_metadata', 'coverages',
                    ['coverage_metadata'])


def downgrade():
    op.drop_index('ix_coverage_metadata', 'coverage_metadata')
    op.drop_column('coverages', 'coverage_metadata')
