"""creacion de equipos

Revision ID: ef56514b8a36
Revises: 459d0e48df4e
Create Date: 2025-11-30 22:20:01.185816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef56514b8a36'
down_revision: Union[str, Sequence[str], None] = '459d0e48df4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('equipo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipo_nombre'), 'equipo', ['nombre'], unique=False)

    op.create_table('integrante',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('equipo_id', sa.Integer(), nullable=False),
        sa.Column('pokemon_id', sa.Integer(), nullable=False),
        sa.Column('apodo', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['equipo_id'], ['equipo.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('integrante_movimiento',
        sa.Column('integrante_id', sa.Integer(), nullable=False),
        sa.Column('movimiento_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['integrante_id'], ['integrante.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['movimiento_id'], ['movimiento.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('integrante_id', 'movimiento_id')
    )

def downgrade() -> None:
    op.drop_table('integrante_movimiento')
    op.drop_table('integrante')
    op.drop_table('equipo')