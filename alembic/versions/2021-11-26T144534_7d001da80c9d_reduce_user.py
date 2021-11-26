"""reduce_user

Revision ID: 7d001da80c9d
Revises: 0e97e22a91d0
Create Date: 2021-11-26 14:45:34.194752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7d001da80c9d"
down_revision = "0e97e22a91d0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_is_active", table_name="users")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_column("users", "role")
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "users",
        sa.Column(
            "role",
            postgresql.ENUM("USER", "ADMIN", name="role"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.create_index("ix_users_is_active", "users", ["is_active"], unique=False)
    # ### end Alembic commands ###
