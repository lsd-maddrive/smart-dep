"""empty message

Revision ID: 0d68fc587a2f
Revises: 
Create Date: 2020-06-21 08:01:37.008274

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0d68fc587a2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('places',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('num', sa.String(length=20), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('attr_os', postgresql.ARRAY(sa.String(length=20)), nullable=True),
    sa.Column('attr_software', postgresql.ARRAY(sa.String(length=20)), nullable=True),
    sa.Column('attr_people', sa.Integer(), nullable=True),
    sa.Column('attr_computers', sa.Integer(), nullable=True),
    sa.Column('attr_blackboard', sa.Boolean(), nullable=True),
    sa.Column('attr_projector', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('avatar_photo', postgresql.BYTEA(), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('devices',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('register_date', sa.DateTime(), nullable=False),
    sa.Column('enabled_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('ip_addr', sa.String(length=20), nullable=True),
    sa.Column('unique_id', sa.String(length=50), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('controller_type', sa.String(length=50), nullable=True),
    sa.Column('code_version', sa.String(length=20), nullable=True),
    sa.Column('is_installed', sa.Boolean(), nullable=True),
    sa.Column('unit_config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('icon_name', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('unique_id')
    )
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('expired_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('commands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('command', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('source_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('states',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('state', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('states')
    op.drop_table('configs')
    op.drop_table('commands')
    op.drop_table('tokens')
    op.drop_table('devices')
    op.drop_table('users')
    op.drop_table('places')
    # ### end Alembic commands ###
