"""changing username name

Revision ID: 6e4f480d4908
Revises: 
Create Date: 2024-10-06 21:08:30.322744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e4f480d4908'
down_revision = None
branch_labels = None
depends_on = None


"""changing username name

Revision ID: 6e4f480d4908
Revises: 
Create Date: 2024-10-06 21:08:30.322744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e4f480d4908'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Create unique constraint on `username` in `user` table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # Step 2: Add `username` column in `wishlist_user` table as nullable=True
    with op.batch_alter_table('wishlist_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=15), nullable=True))

    # Step 3: Copy data from `user_name` to new `username` column
    op.execute("""
        UPDATE wishlist_user
        SET username = (
            SELECT username FROM user WHERE user.username = wishlist_user.user_name
        )
    """)

    # Step 4: Set `username` column to `nullable=False` and add foreign key constraint
    with op.batch_alter_table('wishlist_user', schema=None) as batch_op:
        batch_op.alter_column('username', nullable=False)
        batch_op.create_foreign_key(batch_op.f('fk_wishlist_user_username_user'), 'user', ['username'], ['username'])
        batch_op.drop_column('user_name')


def downgrade():
    # Reverse the above changes
    with op.batch_alter_table('wishlist_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_wishlist_user_username_user'), type_='foreignkey')
        batch_op.drop_column('username')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')
