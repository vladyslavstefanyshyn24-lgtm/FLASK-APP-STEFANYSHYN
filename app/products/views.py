from flask import render_template
from . import products_bp

mock_products = [
    {"id": 1, "name": "Ноутбук"},
    {"id": 2, "name": "Миша"},
    {"id": 3, "name": "Клавіатура"}
]

@products_bp.route('/list')
def product_list():
    return render_template('products/product_list.html', 
                           title="Список Продуктів", 
                           products=mock_products)
