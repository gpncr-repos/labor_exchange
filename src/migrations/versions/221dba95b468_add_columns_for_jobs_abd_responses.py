"""Add columns for jobs abd responses

Revision ID: 221dba95b468
Revises: e6b667630d8a
Create Date: 2023-07-12 12:03:26.466792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '221dba95b468'
down_revision = 'e6b667630d8a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('title', sa.String(), nullable=True, comment='Название вакансии'))
    op.add_column('jobs', sa.Column('description', sa.String(), nullable=True, comment='Описание вакансии'))
    op.add_column('jobs', sa.Column('salary_from', sa.DECIMAL(), nullable=True, comment='Зарплата от'))
    op.add_column('jobs', sa.Column('salary_to', sa.DECIMAL(), nullable=True, comment='Зарплата до'))
    op.add_column('jobs', sa.Column('is_active', sa.Boolean(), nullable=True, comment='Активна ли вакансия'))
    op.add_column('jobs', sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата создания записи'))
    op.add_column('responses', sa.Column('message', sa.String(), nullable=True, comment='Сопроводительное письмо'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('responses', 'message')
    op.drop_column('jobs', 'created_at')
    op.drop_column('jobs', 'is_active')
    op.drop_column('jobs', 'salary_to')
    op.drop_column('jobs', 'salary_from')
    op.drop_column('jobs', 'description')
    op.drop_column('jobs', 'title')
    # ### end Alembic commands ###
