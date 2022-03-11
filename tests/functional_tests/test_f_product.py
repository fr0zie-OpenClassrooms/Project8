from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client

from product.models import Product, Category, Nutriscore


class TestComment(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        # service = Service(executable_path=ChromeDriverManager().install())
        # self.browser = webdriver.Chrome(service=service, options=options)
        service = Service("tests/functional_tests/chromedriver")
        self.browser = webdriver.Chrome(service=service)
        self.client = Client()
        credentials = {
            "username": "TestUser",
            "email": "testuser@purbeurre.fr",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }
        self.client.post(reverse("register"), credentials)

        # Login
        self.browser.get(self.live_server_url + reverse("login"))
        email = self.browser.find_element(By.ID, "email")
        email.send_keys("testuser@purbeurre.fr")
        password = self.browser.find_element(By.ID, "password")
        password.send_keys("t8VhtmOUpYJ39Tb0")
        login = self.browser.find_element(By.ID, "login")
        login.click()

        # Create database objects
        Nutriscore.objects.create(nutriscore="e")
        Category.objects.create(name="Pâtes à tartiner")

        # Create product
        self.product = Product.objects.create(
            name="Nutella",
            description="Pâte à tartiner aux noisettes.",
            brands="Nutella",
            stores="Auchan, Carrefour",
            nutriscore=Nutriscore.objects.get(nutriscore="e"),
            url="https://fr.openfoodfacts.org/produit/59032823/nutella",
            image_url="https://fr.openfoodfacts.org/images/products/59032823/front_fr.155.400.jpg",
            image_nutrition_url="https://fr.openfoodfacts.org/images/products/59032823/nutrition_fr.142.400.jpg",
        )
        self.product.categories.add(Category.objects.get(name="Pâtes à tartiner"))

    def test_comment(self):
        self.browser.get(
            self.live_server_url
            + reverse("details", kwargs={"product_name": "Nutella"})
        )
        comment = self.browser.find_element(By.ID, "comment")
        comment.send_keys("Test comment.")
        submit = self.browser.find_element(By.ID, "submit")
        submit.click()

        self.assertEqual(
            self.browser.find_element(By.ID, "comment").text, "Test comment."
        )
        self.browser.close()
