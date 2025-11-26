"""Crear tabla movimiento_id

Revision ID: 0a7bac8ad7d7
Revises: 48300c5855fb
Create Date: 2025-11-02 17:09:28.429637

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a7bac8ad7d7"
down_revision: Union[str, Sequence[str], None] = "48300c5855fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(  # pylint: disable=no-member
        "movimiento_ide",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("tipo", sa.JSON, nullable=False, server_default="{}"),
        sa.Column("categoria", sa.Text, nullable=False),
        sa.Column("potencia", sa.Integer, nullable=False),
        sa.Column("precision", sa.Integer, nullable=False),
        sa.Column("usos", sa.Integer, nullable=False),
        sa.Column("efecto", sa.Text, nullable=False),
        sa.Column("pokemon_por_huevo", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("pokemon_por_nivel", sa.JSON, nullable=False, server_default="[]"),
        sa.Column("pokemon_por_maquina", sa.JSON, nullable=False, server_default="[]"),
    )

def downgrade() -> None:
    op.drop_table("movimiento_ide")  # pylint: disable=no-member