"""init

Revision ID: fc013e819a2b
Revises: 
Create Date: 2024-05-28 13:07:26.452883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc013e819a2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('experiment',
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=False),
    sa.Column('accum_time', sa.Float(), server_default='0.0', nullable=False),
    sa.Column('vert_res', sa.Float(), server_default='1500.0', nullable=False),
    sa.CheckConstraint('accum_time <= 120', name='check_accum_lime_less_120'),
    sa.CheckConstraint('accum_time >= 0', name='check_accum_time_greater_0'),
    sa.CheckConstraint('vert_res <= 1912.5', name='check_vert_res_less_1912.5'),
    sa.CheckConstraint('vert_res >= 1500', name='check_vert_res_greater_1500'),
    sa.PrimaryKeyConstraint('start_time')
    )
    with op.batch_alter_table('experiment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_experiment_title'), ['title'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('measurement_ch1',
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('prof_len', sa.Integer(), server_default='512', nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('rep_rate', sa.Integer(), nullable=False),
    sa.Column('experiment_time', sa.DateTime(), nullable=False),
    sa.Column('prof_data', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('prof_len <= 1024', name='check_prof_len_less_1024'),
    sa.CheckConstraint('prof_len >= 128', name='check_prof_len_greater_128'),
    sa.ForeignKeyConstraint(['experiment_time'], ['experiment.start_time'], name='fk_experiment_timech1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_ch1_user_id'),
    sa.PrimaryKeyConstraint('start_time')
    )
    op.create_table('measurement_ch2',
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('prof_len', sa.Integer(), server_default='512', nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('rep_rate', sa.Integer(), nullable=False),
    sa.Column('experiment_time', sa.DateTime(), nullable=False),
    sa.Column('prof_data', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('prof_len <= 1024', name='check_prof_len_less_1024'),
    sa.CheckConstraint('prof_len >= 128', name='check_prof_len_greater_128'),
    sa.ForeignKeyConstraint(['experiment_time'], ['experiment.start_time'], name='fk_experiment_timech2'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_ch2_user_id'),
    sa.PrimaryKeyConstraint('start_time')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    op.drop_table('measurement_ch2')
    op.drop_table('measurement_ch1')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('experiment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_experiment_title'))

    op.drop_table('experiment')
    # ### end Alembic commands ###
