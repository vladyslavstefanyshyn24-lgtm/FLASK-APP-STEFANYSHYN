import unittest
from app import app

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        """Тест маршруту /products/list."""
        response = self.client.get("/products/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Список Продуктів", response.data.decode('utf-8'))
        self.assertIn("Ноутбук", response.data.decode('utf-8'))
        self.assertIn("Клавіатура", response.data.decode('utf-8'))
