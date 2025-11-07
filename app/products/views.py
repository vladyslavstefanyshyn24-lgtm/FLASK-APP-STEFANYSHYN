from flask import render_template
from . import products_bp

mock_products = [
    {"id": 1, "name": "Яблуко"},
    {"id": 2, "name": "Банан"},
    {"id": 3, "name": "Авокадо"}
]

@products_bp.route('/list')
def product_list():
    return render_template('products/product_list.html', 
                           title="Список Продуктів", 
                           products=mock_products)
