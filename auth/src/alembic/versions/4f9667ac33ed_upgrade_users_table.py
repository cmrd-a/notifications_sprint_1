"""upgrade users table

Revision ID: 4f9667ac33ed
Revises: dd464d85a95a
Create Date: 2022-11-25 03:25:14.502452

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4f9667ac33ed"
down_revision = "dd464d85a95a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email_confirmed", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("enabled_notifications", sa.ARRAY(sa.String(length=64)), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "enabled_notifications")
    op.drop_column("users", "email_confirmed")
    # ### end Alembic commands ###
