"""create incomes table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cb550454cb63'
down_revision = '5285badbfbdd'
branch_labels = None
depends_on = None


def upgrade():
    # Safely create 'incomes' table only if it doesn't exist
    op.execute("""
    CREATE TABLE IF NOT EXISTS incomes (
        id VARCHAR NOT NULL PRIMARY KEY,
        user_id VARCHAR NOT NULL,
        source VARCHAR NOT NULL,
        description VARCHAR,
        amount FLOAT NOT NULL,
        date DATETIME DEFAULT (CURRENT_TIMESTAMP),
        FOREIGN KEY(user_id) REFERENCES users (id)
    )
    """)

    # Skip altering 'expenses' table for SQLite compatibility
    # SQLite does not support ALTER COLUMN syntax
    # If you really need to enforce NOT NULL, handle it manually in your model or recreate table if necessary.


def downgrade():
    op.execute("DROP TABLE IF EXISTS incomes")