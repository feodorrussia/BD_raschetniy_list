"""Rename name to names

Revision ID: 9dbedd77b2de
Revises: ddaf2df83236
Create Date: 2023-05-11 00:23:03.225165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dbedd77b2de'
down_revision = 'ddaf2df83236'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('awards & penalties', sa.Column('name', sa.String(length=250), nullable=True))
    op.drop_column('awards & penalties', 'name')
    op.add_column('contracts', sa.Column('name', sa.String(length=250), nullable=True))
    op.drop_column('contracts', 'name')
    op.add_column('positions', sa.Column('name', sa.String(length=250), nullable=True))
    op.drop_column('positions', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('name', sa.VARCHAR(length=250), nullable=True))
    op.drop_column('positions', 'name')
    op.add_column('contracts', sa.Column('name', sa.VARCHAR(length=250), nullable=True))
    op.drop_column('contracts', 'name')
    op.add_column('awards & penalties', sa.Column('name', sa.VARCHAR(length=250), nullable=True))
    op.drop_column('awards & penalties', 'name')
    # ### end Alembic commands ###
