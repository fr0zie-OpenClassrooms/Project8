from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client


class TestAuthentification(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        # service = Service(executable_path=ChromeDriverManager().install())
        # self.browser = webdriver.Chrome(service=service, options=options)
        service = Service("tests/functional_tests/chromedriver")
        self.browser = webdriver.Chrome(service=service)

    def test_authentification(self):
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

        self.assertEqual(
            self.browser.find_element(By.ID, "username").text, "TestUser !"
        )
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("account")
        )
        self.browser.close()


class TestForgotPassword(StaticLiveServerTestCase):
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

    def test_reset_password(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "testuser@purbeurre.fr"},
        )
        token = response.context["token"]
        uid = response.context["uid"]

        self.browser.get(
            self.live_server_url
            + reverse("password_reset_confirm", kwargs={"token": token, "uidb64": uid})
        )
        new_password = self.browser.find_element(By.ID, "id_new_password1")
        new_password.send_keys("gH4vB29zZq74nM2O")
        new_password = self.browser.find_element(By.ID, "id_new_password2")
        new_password.send_keys("gH4vB29zZq74nM2O")
        submit = self.browser.find_element(By.ID, "submit")
        submit.click()

        self.browser.get(self.live_server_url + reverse("login"))
        email = self.browser.find_element(By.ID, "email")
        email.send_keys("testuser@purbeurre.fr")
        password = self.browser.find_element(By.ID, "password")
        password.send_keys("gH4vB29zZq74nM2O")
        login = self.browser.find_element(By.ID, "login")
        login.click()

        self.assertEqual(
            self.browser.find_element(By.ID, "username").text, "TestUser !"
        )
        self.browser.close()
