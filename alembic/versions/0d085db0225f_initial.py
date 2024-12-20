"""initial

Revision ID: 0d085db0225f
Revises: 
Create Date: 2024-12-10 21:57:27.768355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d085db0225f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('second_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__author'))
    )
    op.create_index('author_name_index', 'author', ['name', 'second_name'], unique=False)
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name=op.f('fk__book__author_id__author')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__book'))
    )
    op.create_index('book_name_index', 'book', ['name'], unique=False)
    op.create_table('Borrow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('reader_name', sa.String(length=50), nullable=False),
    sa.Column('issue_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.Column('return_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], name=op.f('fk__Borrow__book_id__book')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__Borrow'))
    )
    op.create_index('borrow_reader_index', 'Borrow', ['reader_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('borrow_reader_index', table_name='Borrow')
    op.drop_table('Borrow')
    op.drop_index('book_name_index', table_name='book')
    op.drop_table('book')
    op.drop_index('author_name_index', table_name='author')
    op.drop_table('author')
    # ### end Alembic commands ###
