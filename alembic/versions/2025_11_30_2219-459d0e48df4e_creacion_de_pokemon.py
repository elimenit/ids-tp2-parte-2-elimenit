"""creacion de pokemon

Revision ID: 459d0e48df4e
Revises: 
Create Date: 2025-11-30 22:19:15.086056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '459d0e48df4e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table('tipo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_index('ix_tipo_nombre', 'tipo', ['nombre'], unique=True)

    op.create_table('categoria_movimiento',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('nombre', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

    op.create_table('efecto_movimiento',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('efecto', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pokemon',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.Text, nullable=False),
        sa.Column('species_id', sa.Integer(), nullable=False),
        sa.Column('altura', sa.Float(), nullable=False),
        sa.Column('peso', sa.Float(), nullable=False),
        sa.Column('base_experience', sa.Integer(), nullable=False),
        sa.Column('imagen', sa.Text, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_pokemon_nombre', 'pokemon', ['nombre'])

    op.create_table('estadistica',
        sa.Column('pokemon_id', sa.Integer(), nullable=False),
        sa.Column('puntos_de_golpe', sa.Integer(), nullable=False),
        sa.Column('ataque', sa.Integer(), nullable=False),
        sa.Column('defensa', sa.Integer(), nullable=False),
        sa.Column('ataque_especial', sa.Integer(), nullable=False),
        sa.Column('defensa_especial', sa.Integer(), nullable=False),
        sa.Column('velocidad', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('pokemon_id')
    )

    op.create_table('evolucion',
        sa.Column('from_id', sa.Integer(), nullable=False),
        sa.Column('to_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['from_id'], ['pokemon.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_id'], ['pokemon.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('from_id', 'to_id')
    )

    op.create_table('pokemon_tipo',
        sa.Column('pokemon_id', sa.Integer(), nullable=False),
        sa.Column('tipo_id', sa.Integer(), nullable=False),
        sa.Column('slot', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tipo_id'], ['tipo.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('pokemon_id', 'tipo_id')
    )

    op.create_table('type_efficacy',
        sa.Column('damage_type_id', sa.Integer(), nullable=False),
        sa.Column('target_type_id', sa.Integer(), nullable=False),
        sa.Column('damage_factor', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['damage_type_id'], ['tipo.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_type_id'], ['tipo.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('damage_type_id', 'target_type_id')
    )

    op.create_table('movimiento',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.Text, nullable=False),
        sa.Column('tipo_id', sa.Integer(), nullable=False),
        sa.Column('potencia', sa.Integer(), nullable=True),
        sa.Column('usos', sa.Integer(), nullable=False),
        sa.Column('precision', sa.Integer(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('categoria_id', sa.Integer(), nullable=False),
        sa.Column('efecto_id', sa.Integer(), nullable=False),
        sa.Column('efecto_chance', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['tipo_id'], ['tipo.id']),
        sa.ForeignKeyConstraint(['categoria_id'], ['categoria_movimiento.id']),
        sa.ForeignKeyConstraint(['efecto_id'], ['efecto_movimiento.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_movimiento_nombre', 'movimiento', ['nombre'])

    op.create_table('pokemon_movimiento',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pokemon_id', sa.Integer(), nullable=False),
        sa.Column('move_id', sa.Integer(), nullable=False),
        sa.Column('method_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['move_id'], ['movimiento.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('pokemon_movimiento')
    op.drop_table('movimiento')
    op.drop_table('type_efficacy')
    op.drop_table('pokemon_tipo')
    op.drop_table('evolucion')
    op.drop_table('estadistica')
    op.drop_table('pokemon')
    op.drop_table('efecto_movimiento')
    op.drop_table('categoria_movimiento')
    op.drop_table('tipo')