"""empty message

Revision ID: d8132be74651
Revises: 2d7471abf8b1
Create Date: 2019-09-09 21:41:13.265379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8132be74651'
down_revision = '2d7471abf8b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'venue_name')
    op.drop_column('Show', 'artist_image_link')
    op.drop_column('Show', 'start_time')
    op.drop_column('Show', 'artist_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('start_time', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('artist_image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('venue_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
