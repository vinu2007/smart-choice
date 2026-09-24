from django.test import TestCase
from .models import Product


class ProductModelTest(TestCase):

    def test_product_model_exists(self):
        product = Product()
        self.assertIsNotNone(product)