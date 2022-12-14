"""Add view_count

Revision ID: 996783fda5c2
Revises: 1bfd4ff6d3f8
Create Date: 2022-12-14 17:43:44.978431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '996783fda5c2'
down_revision = '1bfd4ff6d3f8'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'documents',
        sa.Column('view_count', sa.Integer(), nullable=True, server_default="0"),
        schema='guidebook')

    op.add_column(
        'outings',
        sa.Column('enable_view_count', sa.Boolean(), nullable=False, server_default="0"),
        schema='guidebook')
    op.add_column(
        'outings_archives',
        sa.Column('enable_view_count', sa.Boolean(), nullable=False, server_default="0"),
        schema='guidebook')


def downgrade():
    op.drop_column('documents', 'view_count', schema='guidebook')
    op.drop_column('outings', 'enable_view_count', schema='guidebook')
    op.drop_column('outings_archives', 'enable_view_count', schema='guidebook')