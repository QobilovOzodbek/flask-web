"""Add social media links to posts

Revision ID: 9df8196c0751
Revises: 
Create Date: 2024-10-25 10:14:31.959278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9df8196c0751'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.Column('github', sa.String(length=200), nullable=True),
    sa.Column('youtube', sa.String(length=200), nullable=True),
    sa.Column('telegram', sa.String(length=200), nullable=True),
    sa.Column('instagram', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
