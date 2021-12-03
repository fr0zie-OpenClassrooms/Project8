import pytest
from account.models import User


class TestAccountModels:
    @pytest.mark.django_db
    def test_get_user_by_email(self):
        User.objects.create_user(
            username="TestUser",
            email="testuser@purbeurre.fr",
            password="t8VhtmOUpYJ39Tb0",
        )
        user = User.objects.get(email="testuser@purbeurre.fr")
        assert user.username == "TestUser"

    @pytest.mark.django_db
    def test_get_user_by_username(self):
        User.objects.create_user(
            username="TestUser",
            email="testuser@purbeurre.fr",
            password="t8VhtmOUpYJ39Tb0",
        )
        user = User.objects.get(username="TestUser")
        assert user.email == "testuser@purbeurre.fr"
