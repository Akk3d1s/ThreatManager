"""createtable_threat_status

Revision ID: 3ca53d44053b
Revises: d2fa08ccac0c
Create Date: 2021-10-01 18:33:15.237170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ca53d44053b'
down_revision = 'd2fa08ccac0c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('threat_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('threat_status')
