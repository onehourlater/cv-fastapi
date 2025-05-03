import pytest

from fastapi.testclient import TestClient

from tests.constants import TestConstants
from tests.factories.user import UserFactory

from app.user.models import User


@pytest.mark.usefixtures('client')
class TestUser:
    def test_get_user_profile(self, client: TestClient, auth_manager):
        user: User = UserFactory()

        response = client.get(f'/api/v1/users/{user.id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['full_name'] == ''
        assert response_json['kind_of_activity'] == ''
        assert response_json['about'] == ''

    def test_update_user_profile(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        response = authenticated_client.put(
            f'/api/v1/users/{default_user.id}', json=TestConstants.USER_PROFILE_DATA
        )
        assert response.status_code == 200

        response = authenticated_client.get(f'/api/v1/users/{default_user.id}')
        assert response.status_code == 200
        response_json = response.json()
        assert (
            response_json['full_name'] == TestConstants.USER_PROFILE_DATA['full_name']
        )
        assert (
            response_json['kind_of_activity']
            == TestConstants.USER_PROFILE_DATA['kind_of_activity']
        )
        assert response_json['about'] == TestConstants.USER_PROFILE_DATA['about']

    def test_update_user_profile_not_allowed(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        """user_1 tries to change user_2's profile"""
        user_2: User = UserFactory()

        response = authenticated_client.put(
            f'/api/v1/users/{user_2.id}', json=TestConstants.USER_PROFILE_DATA
        )
        assert response.status_code == 403

    def test_update_user_profile_unauthorized(
        self, client: TestClient, default_user: User, auth_manager
    ):
        response = client.put(
            f'/api/v1/users/{default_user.id}', json=TestConstants.USER_PROFILE_DATA
        )
        assert response.status_code == 401


#
