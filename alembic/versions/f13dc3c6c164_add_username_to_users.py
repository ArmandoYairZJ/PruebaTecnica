"""add username to users

Revision ID: f13dc3c6c164
Revises: 0d3082d006ab
Create Date: 2025-11-27 17:07:50.083986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f13dc3c6c164'
down_revision: Union[str, None] = '0d3082d006ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Elimina la restricción de clave foránea antes de cambiar tipos
    op.drop_constraint('logs_user_id_fkey', 'logs', type_='foreignkey')
    # Cambia logs.user_id a String (VARCHAR)
    op.alter_column('logs', 'user_id',
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        postgresql_using='user_id::varchar'
    )
    # Cambia users.id a String (UUID)
    op.alter_column('users', 'id',
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        postgresql_using='id::varchar',
        existing_nullable=False
    )
    # Vuelve a crear la restricción de clave foránea
    op.create_foreign_key(
        'logs_user_id_fkey', 'logs', 'users', ['user_id'], ['id']
    )
    # Agrega columna username
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_nombre', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.drop_column('users', 'nombre')
    # ### end Alembic commands ###

def downgrade() -> None:
    # Elimina la restricción de clave foránea antes de revertir tipos
    op.drop_constraint('logs_user_id_fkey', 'logs', type_='foreignkey')
    # Revertir logs.user_id a Integer
    op.alter_column('logs', 'user_id',
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        postgresql_using='user_id::integer'
    )
    # Revertir users.id a Integer
    op.alter_column('users', 'id',
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        postgresql_using='id::integer',
        existing_nullable=False
    )
    # Vuelve a crear la restricción de clave foránea
    op.create_foreign_key(
        'logs_user_id_fkey', 'logs', 'users', ['user_id'], ['id']
    )
    op.add_column('users', sa.Column('nombre', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_nombre', 'users', ['nombre'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.drop_column('users', 'username')
    # ### end Alembic commands ###