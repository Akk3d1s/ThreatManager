"""createtable_threat_category

Revision ID: 4bb07abba012
Revises: 3547414a9813
Create Date: 2021-10-02 18:38:32.292877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bb07abba012'
down_revision = '3547414a9813'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('threat_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('threat_category')
