import pytest
from django.urls import reverse
from django.test import Client
from product.models import Product, Category, Nutriscore


class TestProductViews:
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
    def test_product_found(self):
        client = Client()
        response = client.get(reverse("search"), {"product": "Test Product"})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_product_not_found(self):
        client = Client()
        response = client.get(reverse("search"), {"product": "Random Product"})
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_product_details_found(self):
        client = Client()
        path = reverse("details", kwargs={"product_name": "Test Product"})
        response = client.get(path)
        assert response.context.get("product") != None
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_product_details_not_found(self):
        client = Client()
        path = reverse("details", kwargs={"product_name": "Random Product"})
        response = client.get(path)
        assert response.context.get("product") == None
        assert response.status_code == 404
