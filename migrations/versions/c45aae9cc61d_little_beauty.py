"""Little beauty

Revision ID: c45aae9cc61d
Revises: 55026979b265
Create Date: 2023-05-11 06:06:16.340770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45aae9cc61d'
down_revision = '55026979b265'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contracts', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contracts', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###
