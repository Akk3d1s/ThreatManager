"""createtables

Revision ID: bf837abb5002
Revises: 
Create Date: 2021-10-05 00:06:29.412149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf837abb5002'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('surename', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'],['user_role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    op.create_table('threat_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('threat_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('threat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('reproduce_steps', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['threat_status.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['threat_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threat_timestamp'), 'threat', ['timestamp'], unique=False)
    
    op.create_table('attachment_extension',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('extension', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('threat_attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('threat_id', sa.Integer(), nullable=True),
    sa.Column('extension_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['threat_id'], ['threat.id'], ),
    sa.ForeignKeyConstraint(['extension_id'], ['extension.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_index(op.f('ix_threat_attachment_timestamp'), 'threat_attachment', ['timestamp'], unique=False)

    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=140), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True), 
    sa.Column('threat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['threat_id'], ['threat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('comment_attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('extension_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['extension_id'], ['extension.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_index(op.f('ix_comment_attachment_timestamp'), 'comment_attachment', ['timestamp'], unique=False)


def downgrade():
    op.drop_table('comment_attachment')
    op.drop_table('comment')
    op.drop_table('threat_attachment')
    op.drop_table('attachment_extension')
    op.drop_index(op.f('ix_threat_timestamp'), table_name='threat')
    op.drop_table('threat')
    # op.drop_index(op.f('ix_threat_attachment_timestamp'), table_name='threat_attachment')
    op.drop_table('threat_category')
    op.drop_table('threat_status')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('user_role')
    



