"""creado_tablas_pokemon

Revision ID: 44f84e44f904
Revises: 0a7bac8ad7d7
Create Date: 2025-11-20 00:48:10.301371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44f84e44f904'
down_revision: Union[str, Sequence[str], None] = '0a7bac8ad7d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pokemon_tipo",
        sa.Column("pokemon_id", sa.Integer,nullable=False),
        sa.Column("tipo_id", sa.Integer, nullable=False),
        sa.Column("slot", sa.Integer)
    )
    op.create_table(
        "tipo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
    )
    
    op.create_table(
        "pokemon",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("imagen", sa.Text, nullable=False),
        sa.Column("altura", sa.Integer),
        sa.Column("peso", sa.Integer),
        sa.Column("base_experience", sa.Integer)
    )
    
    op.create_table(
        "type_efficacy",
        sa.Column("damage_type_id", sa.Integer, nullable=False),
        sa.Column("target_type_id", sa.Integer, nullable=False),
        sa.Column("damage_factor", sa.Integer, nullable=False)
    )
    op.create_table(
        "estadistica",
        sa.Column("pokemon_id", sa.Integer, sa.ForeignKey("pokemon.id"), primary_key=True),
        sa.Column("puntos_de_golpe", sa.Integer, nullable=False),
        sa.Column("ataque", sa.Integer, nullable=False),
        sa.Column("defensa", sa.Integer, nullable=False),
        sa.Column("ataque_especial", sa.Integer, nullable=False),
        sa.Column("defensa_especial", sa.Integer, nullable=False),
        sa.Column("velocidad", sa.Integer, nullable=False),
    )
    op.create_table(
        "evolucion",
        sa.Column("from_id", sa.Integer, nullable=False),
        sa.Column("to_id", sa.Integer, nullable=False),
    )
    op.create_table(
        "categoria_movimiento",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("nombre", sa.Text, nullable=False)
    )
    op.create_table(
        "efecto_movimiento",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("efecto", sa.Text, nullable=False)
    )
    op.create_table(
        "movimiento",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("tipo_id", sa.Integer, nullable=False),
        sa.Column("potencia", sa.Integer),
        sa.Column("usos", sa.Integer, nullable=False),
        sa.Column("precision", sa.Integer, nullable=False),
        sa.Column("priority", sa.Integer, nullable=False),
        sa.Column("target_id", sa.Integer, nullable=False),
        sa.Column("categoria_id", sa.Integer, nullable=False),
        sa.Column("efecto_id", sa.Integer, nullable=False),
        sa.Column("efecto_chance", sa.Integer)
    )
    op.create_table(
        "pokemon_movimiento",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("pokemon_id", sa.Integer, nullable=False),
        sa.Column("move_id", sa.Integer, nullable=False),
        sa.Column("method_id", sa.Integer, nullable=False)
    )
    #Endpoint de movimientos

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
    """Downgrade schema."""
    op.drop_table("pokemon_tipo")
    op.drop_table("tipo")
    op.drop_table("pokemon")
    op.drop_table("type_efficacy")
    op.drop_table("estadistica")
    op.drop_table("evolucion")
    op.drop_table("categoria_movimiento")
    op.drop_table("movimiento")
    op.drop_table("pokemon_movimiento")
    op.drop_table("movimiento_ide")    