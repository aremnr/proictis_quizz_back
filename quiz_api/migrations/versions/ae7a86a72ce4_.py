"""empty message

Revision ID: ae7a86a72ce4
Revises: 95067945f9dc
Create Date: 2024-07-28 22:22:44.712820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae7a86a72ce4'
down_revision: Union[str, None] = '95067945f9dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('quizzes',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('dis', sa.String(), nullable=False),
                    sa.Column('owner_id', sa.String(), nullable=False),
                    sa.Column('question_count', sa.Integer(), nullable=False),
                    sa.Column('all_points', sa.Integer(), nullable=False),
                    sa.Column('create_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('questions',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('quiz_id', sa.UUID(), nullable=False),
                    sa.Column('question_text', sa.String(), nullable=False),
                    sa.Column('points', sa.Integer(), nullable=False),
                    sa.Column('right_answer', sa.Integer(), nullable=False),
                    sa.Column('pcl', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('answers',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('question_id', sa.UUID(), nullable=False),
                    sa.Column('answer_text', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('answers')
    op.drop_table('questions')
    op.drop_table('quizzes')
