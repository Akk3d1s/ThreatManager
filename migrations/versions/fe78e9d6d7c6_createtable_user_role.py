"""createtable_user_role

Revision ID: fe78e9d6d7c6
Revises: d72965ecd52f
Create Date: 2021-10-02 18:52:17.742649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe78e9d6d7c6'
down_revision = 'd72965ecd52f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user_role')
