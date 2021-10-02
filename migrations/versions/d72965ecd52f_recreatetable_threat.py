"""recreatetable_threat

Revision ID: d72965ecd52f
Revises: 4bb07abba012
Create Date: 2021-10-02 18:39:12.159798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72965ecd52f'
down_revision = '4bb07abba012'
branch_labels = None
depends_on = None


def upgrade():
    # drop old threat table
    op.drop_index(op.f('ix_threat_timestamp'), table_name='threat')
    op.drop_table('threat')
    # create new threat table
    op.create_table('threat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('recreation_steps', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('attachment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['threat_status.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['threat_category.id'], ),
    sa.ForeignKeyConstraint(['attachment_id'], ['threat_attachment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threat_timestamp'), 'threat', ['timestamp'], unique=False)


def downgrade():
    # drop new threat table
    op.drop_index(op.f('ix_threat_timestamp'), table_name='threat')
    op.drop_table('threat')
    # create old threat table
    op.create_table('threat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threat_timestamp'), 'threat', ['timestamp'], unique=False)
