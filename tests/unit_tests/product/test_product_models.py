import pytest
from product.models import Product, Category, Nutriscore
from product.fill import Fill


class TestProductModels:
    def setup_method(self):
        Nutriscore.objects.create(nutriscore="a")
        Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="A product to test.",
            brands="Test Brand",
            stores="Store A, Store B",
            nutriscore=Nutriscore.objects.get(nutriscore="a"),
            url="https://www.purbeurre.fr/tests/test_product.html",
            image_url="https://www.purbeurre.fr/tests/test_product.png",
            image_nutrition_url="https://www.purbeurre.fr/tests/test_product.html",
        )
        self.product.categories.add(Category.objects.get(name="Test Category"))

    @pytest.mark.django_db
    def test_get_product(self):
        product_name = "Test Product"
        product = Product.get_product(product_name)
        assert product.name == "Test Product"

    @pytest.mark.django_db
    def test_find_substitute(self):
        product_name = "Test Product"
        product = Product.objects.get(name=product_name)
        substitutes = Product.find_substitute(product)
        for substitute in substitutes:
            assert substitute.nutriscore.nutriscore < product.nutriscore.nutriscore


class TestProductFill:
    def setup_method(self):
        self.fill = Fill()
        self.fill.add_nutriscores()

    @pytest.mark.django_db
    def test_get_products(self, mocker):
        mocker.patch("product.fill.requests.get", side_effect=mocked_requests_get)
        self.fill.get_products(1, 100)
        assert "products" in self.fill.raw_products.json()

    @pytest.mark.django_db
    def test_clean_products(self, mocker):
        mocker.patch("product.fill.requests.get", side_effect=mocked_requests_get)
        self.fill.get_products(1, 100)
        self.fill.clean_products()
        assert len(self.fill.cleaned_products) == 1

    @pytest.mark.django_db
    def test_cleaned_products_contains_all_fields(self, mocker):
        mocker.patch("product.fill.requests.get", side_effect=mocked_requests_get)
        self.fill.get_products(1, 100)
        self.fill.clean_products()
        for product, categories in self.fill.cleaned_products:
            assert product.name
            assert product.description
            assert product.brands
            assert product.nutriscore
            assert product.url
            assert product.image_url
            for category in categories:
                assert category

    @pytest.mark.django_db
    def test_cleaned_products_found_in_database(self, mocker):
        mocker.patch("product.fill.requests.get", side_effect=mocked_requests_get)
        self.fill.get_products(1, 100)
        self.fill.clean_products()
        self.fill.create_products_and_categories()
        for product, categories in self.fill.cleaned_products:
            assert Product.objects.get(name=product.name)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    products = {
        "products": [
            {
                "brands": "Valid brand",
                "categories": "Valid category",
                "categories_lc": "fr",
                "generic_name_fr": "Valid description",
                "image_url": "http://localhost:5000/valid_image.png",
                "image_nutrition_url": "http://localhost:5000/valid_image.png",
                "nutrition_grade_fr": "a",
                "product_name": "Valid product",
                "stores": "Valid stores",
                "url": "http://localhost:5000/valid_url.html",
            },
            {
                "brands": "Valid brand",
                "categories": "Valid category",
                "categories_lc": "Unvalid lang",
                "generic_name_fr": "Valid description",
                "image_url": "http://localhost:5000/valid_image.png",
                "image_nutrition_url": "http://localhost:5000/valid_image.png",
                "nutrition_grade_fr": "b",
                "product_name": "Valid product",
                "stores": "Valid stores",
                "url": "http://localhost:5000/valid_url.html",
            },
            {
                "brands": "",
                "categories": "",
                "categories_lc": "",
                "generic_name_fr": "",
                "image_url": "",
                "image_nutrition_url": "",
                "nutrition_grade_fr": "b",
                "product_name": "Unvalid product",
                "stores": "",
                "url": "",
            },
        ]
    }

    return MockResponse(products, 200)
