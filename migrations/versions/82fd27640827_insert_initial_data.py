"""Insert initial data

Revision ID: 82fd27640827
Revises: 891d33fe4ff3
Create Date: 2025-12-11 21:44:17.323240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer, String, Float, Boolean

# revision identifiers, used by Alembic.
revision = '82fd27640827'
down_revision = '891d33fe4ff3'
branch_labels = None
depends_on = None

categories_table = table('categories',
    column('id', Integer),
    column('name', String)
)

products_table = table('products',
    column('id', Integer),
    column('name', String),
    column('price', Float),
    column('active', Boolean),
    column('created_at', sa.DateTime),
    column('category_id', Integer)
)

def upgrade():
    op.bulk_insert(categories_table, [
        {"name": "Electronics"},
        {"name": "Books"},
        {"name": "Clothing"},
    ])
    op.bulk_insert(products_table, [
        {"name": "Gaming Laptop",   "price": 1899.99, "active": True,  "category_id": 1},
        {"name": "Python Book",     "price": 49.99,   "active": True,  "category_id": 2},
        {"name": "Winter Jacket",   "price": 129.99,  "active": False, "category_id": 3},
    ])


def downgrade():
    op.execute("DELETE FROM products WHERE name IN ('Gaming Laptop', 'Python Book', 'Winter Jacket')")
    op.execute("DELETE FROM categories WHERE name IN ('Electronics', 'Books', 'Clothing')")