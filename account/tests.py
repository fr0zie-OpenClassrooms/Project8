from django.test import TestCase
from django.urls import reverse

from account.models import User
from account.forms import RegistrationForm


class BaseTest(TestCase):
    def setUp(self):
        self.user = {
            "username": "TestUser",
            "email": "testuser@purbeurre.fr",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }
        self.register_url = reverse("register")
        self.login_url = reverse("login")


class RegistrationTest(BaseTest):
    def test_user_registration_form(self):
        form = RegistrationForm(data=self.user)
        self.assertTrue(form.is_valid())

    def test_user_page_access(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 302)


class LoginTest(BaseTest):
    def test_user_page_access(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_user_cant_login(self):
        response = self.client.post(self.login_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 400)


class UserTest(BaseTest):
    def setUp(self):
        User.objects.create_user(
            username="TestUser",
            email="testuser@purbeurre.fr",
            password="t8VhtmOUpYJ39Tb0",
        )

    def test_get_user_by_email(self):
        user = User.objects.get(email="testuser@purbeurre.fr")
        self.assertEqual(user.username, "TestUser")

    def test_get_user_by_username(self):
        user = User.objects.get(username="TestUser")
        self.assertEqual(user.email, "testuser@purbeurre.fr")
