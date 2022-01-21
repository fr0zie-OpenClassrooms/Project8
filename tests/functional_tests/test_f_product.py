import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from product.models import Product, Category, Nutriscore


class TestProduct(StaticLiveServerTestCase):
    @pytest.mark.django_db
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

        # Create products
        Nutriscore.objects.create(nutriscore="b")
        Nutriscore.objects.create(nutriscore="c")
        Nutriscore.objects.create(nutriscore="e")
        Category.objects.create(name="Pâtes à tartiner")

        # Searched product
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

        # First substitute
        self.substitute1 = Product.objects.create(
            name="Tartimouss",
            description="Pâte à tartiner aux noisettes.",
            brands="Tartimouss",
            stores="Auchan, Carrefour",
            nutriscore=Nutriscore.objects.get(nutriscore="b"),
            url="https://fr.openfoodfacts.org/produit/3770012968304/tartimouss-noisette-cacao-et-lait-graine-de-choc",
            image_url="https://fr.openfoodfacts.org/images/products/377/001/296/8304/front_fr.3.400.jpg",
            image_nutrition_url="https://fr.openfoodfacts.org/images/products/377/001/296/8304/nutrition_fr.5.400.jpg",
        )
        self.substitute1.categories.add(Category.objects.get(name="Pâtes à tartiner"))

        # Second substitute
        self.substitute2 = Product.objects.create(
            name="Kaonuts",
            description="Pâte à tartiner aux noisettes.",
            brands="Carrefour",
            stores="Carrefour",
            nutriscore=Nutriscore.objects.get(nutriscore="c"),
            url="https://fr.openfoodfacts.org/produit/3560071269753/kaonuts-carrefour",
            image_url="https://fr.openfoodfacts.org/images/products/356/007/126/9753/front_fr.12.400.jpg",
            image_nutrition_url="https://fr.openfoodfacts.org/images/products/356/007/126/9753/ingredients_fr.9.400.jpg",
        )
        self.substitute2.categories.add(Category.objects.get(name="Pâtes à tartiner"))

        # Register
        self.browser.get(self.live_server_url + reverse("register"))
        username = self.browser.find_element(By.ID, "username")
        username.send_keys("TestUser")
        email = self.browser.find_element(By.ID, "email")
        email.send_keys("testuser@purbeurre.fr")
        password1 = self.browser.find_element(By.ID, "password1")
        password1.send_keys("t8VhtmOUpYJ39Tb0")
        password2 = self.browser.find_element(By.ID, "password2")
        password2.send_keys("t8VhtmOUpYJ39Tb0")
        register = self.browser.find_element(By.ID, "register")
        register.click()

        # Login
        email = self.browser.find_element(By.ID, "email")
        email.send_keys("testuser@purbeurre.fr")
        password = self.browser.find_element(By.ID, "password")
        password.send_keys("t8VhtmOUpYJ39Tb0")
        login = self.browser.find_element(By.ID, "login")
        login.click()

    def test_search_and_save_substitute(self):
        # Search for 'Nutella'
        self.browser.get(self.live_server_url + reverse("home"))
        search = self.browser.find_element(By.NAME, "search-request")
        search.send_keys("Nutella")
        search.send_keys(Keys.RETURN)

        # Save substitute
        save_button = self.browser.find_element(By.CLASS_NAME, "btn-primary")
        save_button.click()

        self.assertEqual(
            self.browser.find_element(By.ID, "substitute").text, "Tartimouss"
        )
        self.assertEqual(self.browser.find_element(By.ID, "product").text, "Nutella")
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("substitutes")
        )
        self.browser.close()

    def test_search_and_view_substitute_details(self):
        # Search for 'Nutella'
        self.browser.get(self.live_server_url + reverse("home"))
        search = self.browser.find_element(By.ID, "search")
        search.send_keys("Nutella")
        search.send_keys(Keys.RETURN)

        # View first substitute details
        substitute = self.browser.find_element(By.CLASS_NAME, "img")
        substitute.click()

        self.assertEqual(self.browser.find_element(By.ID, "product").text, "Tartimouss")
        self.browser.close()
