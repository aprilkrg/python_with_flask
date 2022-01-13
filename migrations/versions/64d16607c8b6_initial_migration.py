"""initial-migration

Revision ID: 64d16607c8b6
Revises: 
Create Date: 2022-01-12 17:53:25.321439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d16607c8b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table(
        'users'
    )
