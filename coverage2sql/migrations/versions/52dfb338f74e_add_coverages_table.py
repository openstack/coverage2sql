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

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('coverages',
                    sa.Column('id', sa.BigInteger(), primary_key=True),
                    sa.Column('project_name', sa.String(256), nullable=False),
                    sa.Column('coverage_rate', sa.Float()),
                    sa.Column('report_time', sa.DateTime()),
                    sa.Column('report_time_microsecond', sa.Integer(),
                              default=0),
                    mysql_engine='InnoDB')


def downgrade():
    raise NotImplementedError()
