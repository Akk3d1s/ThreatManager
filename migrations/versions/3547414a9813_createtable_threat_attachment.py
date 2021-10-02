"""createtable_threat_attachment

Revision ID: 3547414a9813
Revises: 3ca53d44053b
Create Date: 2021-10-01 21:04:55.391715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3547414a9813'
down_revision = '3ca53d44053b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('attachment_extension',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('extension', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('threat_attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('extension_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['extension_id'], ['extension.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threat_attachment_timestamp'), 'threat_attachment', ['timestamp'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_threat_attachment_timestamp'), table_name='threat_attachment')
    op.drop_table('threat_attachment')
    op.drop_table('attachment_extension')
