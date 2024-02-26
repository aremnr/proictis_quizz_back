"""DataBase

Revision ID: 5fc63caceb46
Revises: df85eaabd7b4
Create Date: 2024-02-26 22:20:11.777643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fc63caceb46'
down_revision: Union[str, None] = 'df85eaabd7b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('answer_text', sa.String(), nullable=True))
    op.drop_index('ix_answers_answer', table_name='answers')
    op.drop_column('answers', 'answer')
    op.add_column('questions', sa.Column('question_text', sa.String(), nullable=True))
    op.drop_index('ix_questions_question', table_name='questions')
    op.drop_column('questions', 'question')
    op.add_column('quizzes', sa.Column('quiz_name', sa.String(), nullable=True))
    op.create_index(op.f('ix_quizzes_quiz_name'), 'quizzes', ['quiz_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_quizzes_quiz_name'), table_name='quizzes')
    op.drop_column('quizzes', 'quiz_name')
    op.add_column('questions', sa.Column('question', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_questions_question', 'questions', ['question'], unique=False)
    op.drop_column('questions', 'question_text')
    op.add_column('answers', sa.Column('answer', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_answers_answer', 'answers', ['answer'], unique=False)
    op.drop_column('answers', 'answer_text')
    # ### end Alembic commands ###
