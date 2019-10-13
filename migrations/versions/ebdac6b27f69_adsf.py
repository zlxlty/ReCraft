"""adsf

Revision ID: ebdac6b27f69
Revises: 
Create Date: 2019-07-30 20:09:06.592659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebdac6b27f69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('picturesets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dirname', sa.String(length=64), nullable=True),
    sa.Column('prediction', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_picturesets_dirname'), 'picturesets', ['dirname'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('cover', sa.String(length=64), nullable=True),
    sa.Column('dirname', sa.String(length=64), nullable=True),
    sa.Column('materials', sa.String(length=256), nullable=True),
    sa.Column('difficulties', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_videos_difficulties'), 'videos', ['difficulties'], unique=False)
    op.create_index(op.f('ix_videos_materials'), 'videos', ['materials'], unique=False)
    op.create_index(op.f('ix_videos_title'), 'videos', ['title'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_index(op.f('ix_videos_title'), table_name='videos')
    op.drop_index(op.f('ix_videos_materials'), table_name='videos')
    op.drop_index(op.f('ix_videos_difficulties'), table_name='videos')
    op.drop_table('videos')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_picturesets_dirname'), table_name='picturesets')
    op.drop_table('picturesets')
    # ### end Alembic commands ###