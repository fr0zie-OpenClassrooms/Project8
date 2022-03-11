import pytest
from django.urls import reverse
from django.test import Client
from django.contrib import auth


@pytest.mark.django_db
def test_login_route():
    client = Client()
    credentials = {
        "username": "TestUser",
        "email": "testuser@purbeurre.fr",
        "password1": "t8VhtmOUpYJ39Tb0",
        "password2": "t8VhtmOUpYJ39Tb0",
    }
    client.post(reverse("register"), credentials)
    response = client.post(
        reverse("login"),
        {"email": "testuser@purbeurre.fr", "password": "t8VhtmOUpYJ39Tb0"},
    )
    user = auth.get_user(client)

    assert response.status_code == 302
    assert response.url == reverse("account")
    assert user.is_authenticated
