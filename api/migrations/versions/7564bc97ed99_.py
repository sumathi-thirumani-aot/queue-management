"""empty message

Revision ID: 7564bc97ed99
Revises: 92cd814a5c05
Create Date: 2019-11-11 13:11:55.384979

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '7564bc97ed99'
down_revision = '47c80f6b0123'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exam', sa.Column('bcmp_job_id', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exam', 'bcmp_job_id')
    # ### end Alembic commands ###