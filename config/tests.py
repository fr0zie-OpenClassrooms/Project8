from django.test import TestCase

from product.models import Product
from .fill import Fill


class FillTest(TestCase):
    def setUp(self):
        self.fill = Fill()
        self.raw_products = [
            {
                "brands": "Valid brand",
                "categories": "Valid category",
                "categories_lc": "fr",
                "code": "1",
                "generic_name_fr": "Valid description",
                "image_url": "http://localhost:5000/valid_image.png",
                "nutrition_grade_fr": "a",
                "product_name": "Valid product",
                "stores": "Valid stores",
                "url": "http://localhost:5000/valid_url.html",
            },
            {
                "brands": "Valid brand",
                "categories": "Valid category",
                "categories_lc": "Unvalid lang",
                "code": "2",
                "generic_name_fr": "Valid description",
                "image_url": "http://localhost:5000/valid_image.png",
                "nutrition_grade_fr": "b",
                "product_name": "Valid product",
                "stores": "Valid stores",
                "url": "http://localhost:5000/valid_url.html",
            },
            {
                "brands": "",
                "categories": "",
                "categories_lc": "",
                "code": "0",
                "generic_name_fr": "",
                "image_url": "",
                "nutrition_grade_fr": "b",
                "product_name": "Unvalid product",
                "stores": "",
                "url": "",
            },
        ]

    def test_get_products(self):
        self.fill.get_products(1, 10)
        self.assertTrue("products" in self.fill.raw_products.json())

    def test_clean_products(self):
        self.fill.products.extend(self.raw_products)
        self.fill.clean_products()
        self.assertTrue(len(self.fill.cleaned_products) == 1)

    def test_cleaned_products_contains_all_fields(self):
        self.fill.get_products(1, 10)
        self.fill.clean_products()
        for product, categories in self.fill.cleaned_products:
            self.assertTrue(product.name)
            self.assertTrue(product.description)
            self.assertTrue(product.brands)
            self.assertTrue(product.nutriscore)
            self.assertTrue(product.url)
            self.assertTrue(product.image_url)
            for category in categories:
                self.assertTrue(category)

    def test_cleaned_products_found_in_database(self):
        self.fill.get_products(1, 10)
        self.fill.clean_products()
        self.fill.create_products_and_categories()
        for product, categories in self.fill.cleaned_products:
            prod = Product.objects.get(name=product.name)
            self.assertTrue(prod)
