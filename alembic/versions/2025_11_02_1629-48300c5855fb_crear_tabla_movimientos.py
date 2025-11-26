"""Crear tabla movimientos

Revision ID: 48300c5855fb
Revises:
Create Date: 2025-11-02 16:29:14.703122

"""

from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "48300c5855fb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # pylint: disable=no-member
        "movimientos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("tipo", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("categoria", sa.Text, nullable=False),
        sa.Column("potencia", sa.Integer, nullable=False),
        sa.Column("precision", sa.Integer, nullable=False),
        sa.Column("usos", sa.Integer, nullable=False),
        sa.Column("efecto", sa.Text, nullable=False),
    )

def downgrade() -> None:
    op.drop_table("movimientos")  # pylint: disable=no-member
