"""agreguo equipos y mienbros

Revision ID: bf8d39d8dd9d
Revises: 44f84e44f904
Create Date: 2025-11-20 11:44:38.944307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf8d39d8dd9d'
down_revision: Union[str, Sequence[str], None] = '44f84e44f904'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
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
    op.create_table('equipo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_equipo_nombre'), 'equipo', ['nombre'])

    op.create_table('integrante',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('apodo', sa.String(), nullable=True),
        sa.Column('pokemon_id', sa.Integer(), nullable=False),
        sa.Column('equipo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['equipo_id'], ['equipo.id']),
        sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('movimiento_integrante',
        sa.Column('integrante_id', sa.Integer(), nullable=False),
        sa.Column('movimiento_id', sa.Integer(), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['integrante_id'], ['integrante.id']),
        sa.ForeignKeyConstraint(['movimiento_id'], ['movimiento.id']),
        sa.PrimaryKeyConstraint('integrante_id', 'movimiento_id')
    )
def downgrade():
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
    op.drop_table("equipo")
    op.drop_table("integrante")
    op.drop_table("movimiento_integrante")