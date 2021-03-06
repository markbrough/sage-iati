"""empty message

Revision ID: a5009bf8f137
Revises: 14276c52a49c
Create Date: 2020-05-10 16:32:33.667543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5009bf8f137'
down_revision = '14276c52a49c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organisationfunder_incomingfunds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organisation_slug', sa.UnicodeText(), nullable=False),
    sa.Column('organisationfunder_id', sa.Integer(), nullable=False),
    sa.Column('account_number', sa.UnicodeText(), nullable=True),
    sa.Column('funding_org_activity_id', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['organisation_slug'], ['organisation.organisation_slug'], ),
    sa.ForeignKeyConstraint(['organisationfunder_id'], ['organisationfunder.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('organisation_slug', 'account_number', name='organisationfunder_incomingfunds')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organisationfunder_incomingfunds')
    # ### end Alembic commands ###
