import pytest
from django.urls import reverse
from django.test import Client
from account.forms import RegistrationForm


class TestAccountViews:
    def setup_method(self):
        self.user = {
            "username": "TestUser",
            "email": "testuser@purbeurre.fr",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    @pytest.mark.django_db
    def test_user_registration_form(self):
        form = RegistrationForm(data=self.user)
        assert form.is_valid() == True

    @pytest.mark.django_db
    def test_user_page_access(self):
        client = Client()
        response = client.get(self.register_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_registration(self):
        client = Client()
        response = client.post(self.register_url, self.user, format="text/html")
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_user_page_access(self):
        client = Client()
        response = client.get(self.login_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_cant_login(self):
        client = Client()
        response = client.post(self.login_url, self.user, format="text/html")
        assert response.status_code == 400
