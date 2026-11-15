"""Создаёт таблицу masters

Revision ID: 0001_create_masters
Revises:
Create Date: 2026-11-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_masters"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("specialization", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_masters_id"), "masters", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_masters_id"), table_name="masters")
    op.drop_table("masters")
