import pytest

from fastapi.testclient import TestClient

from tests.factories.user import UserFactory

from app.user.models import User
from app.auth.manager import AuthManager


@pytest.mark.usefixtures('client')
class TestAuth:
    # TODO: check access with auth token after username changed

    def test_signup(self, client: TestClient):
        response = client.post(
            '/api/v1/signup',
            json={
                'email': 'hello@gmail.com',
                'password': 'kitty',
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'email': 'hello@gmail.com',
            'username': 'hello',
        }

        response = client.post(
            '/api/v1/signup',
            json={
                'email': 'hello@mail.ru',
                'password': 'kitty',
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            'id': 2,
            'email': 'hello@mail.ru',  # different Email
            'username': 'hello-2',
        }

    def test_signup_already_exists(self, client: TestClient, auth_manager: AuthManager):
        user: User = UserFactory()

        response = client.post(
            '/api/v1/signup',
            json={
                'email': user.email,
                'password': 'kitty',
            },
        )
        assert response.status_code == 400

    def test_signup_no_email(self, client: TestClient):
        response = client.post('/api/v1/signup', json={})
        assert response.status_code == 422

    def test_signin(self, client: TestClient, auth_manager: AuthManager):
        # TODO:
        pass

    def test_me(self, authenticated_client: TestClient):
        response = authenticated_client.get('/api/v1/me')
        print()
        print('response.json(): ', response.json())

    """
    def test_get_user(self, client: TestClient, auth_manager):
        print()
        print('[test_get_user] auth_manager: ', auth_manager)

        auth_manager.signup(auth_schema.UserBaseAuth(email='hello@gmail.com', password=TestConstants.USER_PASSWORD))

        response = client.get('/api/v1/users/1')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['email'] == 'hello@gmail.com'
        assert response_json['username'] == 'hello'
    """


#
