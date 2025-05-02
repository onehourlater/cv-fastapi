import pytest

from fastapi.testclient import TestClient

from tests.constants import TestConstants
from tests.factories.cv import CVFactory

from app.user.models import User
from app.cv.models import CV


@pytest.mark.usefixtures('client')
class TestCV:
    def test_create_cv(self, authenticated_client: TestClient, auth_manager):
        response = authenticated_client.post(
            '/api/v1/cvs/',
            json={
                'about': TestConstants.CV_ABOUT,
            },
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['about'] == TestConstants.CV_ABOUT

    def test_get_cvs(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.get('/api/v1/cvs/')
        assert response.status_code == 200
        response_json = response.json()
        response_json_cv = response_json[0]
        assert response_json_cv['about'] == cv.about


#
