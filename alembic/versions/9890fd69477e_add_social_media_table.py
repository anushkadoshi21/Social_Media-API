"""add social media table

Revision ID: 9890fd69477e
Revises: 7dfcf7aaa3b3
Create Date: 2021-12-09 13:34:10.612538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '9890fd69477e'
down_revision = '7dfcf7aaa3b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('social_media',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_published', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIME(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='social_media_pkey')
    )


def downgrade():
    op.drop_table('social_media')
