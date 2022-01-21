from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class TestAuthentification(StaticLiveServerTestCase):
    def test_authentification(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

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
