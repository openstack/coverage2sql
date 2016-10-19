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

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('coverages', sa.Column('test_type', sa.String(256),
                  nullable=False, server_default='py27'))
    op.create_index('ix_test_type', 'coverages', ['test_type'])


def downgrade():
    op.drop_index('ix_test_type', 'coverages')
    op.drop_column('coverages', 'test_type')
