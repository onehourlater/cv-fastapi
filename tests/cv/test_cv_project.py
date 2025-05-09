import pytest
from fastapi.testclient import TestClient

from tests.constants import TestConstants
from tests.factories.cv import CVFactory

from app.user.models import User
from app.cv.models import CV


@pytest.mark.usefixtures('client')
class TestCVProject:
    def test_get_cv_projects(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.get(f'/api/v1/cvs/{cv.id}/projects')
        assert response.status_code == 200

    def test_get_cv_projects_no_permissions(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        cv: CV = CVFactory()

        response = authenticated_client.get(f'/api/v1/cvs/{cv.id}/projects')
        assert response.status_code == 403

    def test_create_cv_project(
        self, authenticated_client: TestClient, default_user: User, auth_manager
    ):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.post(
            f'/api/v1/cvs/{cv.id}/projects',
            json={
                'title': TestConstants.CV_PROJECT_TITLE,
                'end_date': TestConstants.CV_PROJECT_END_DATE,
                'role': TestConstants.CV_PROJECT_ROLE,
                'link': TestConstants.CV_PROJECT_LINK,
                'description': TestConstants.CV_PROJECT_DESCRIPTION,
            },
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == TestConstants.CV_PROJECT_TITLE
        assert response_json['end_date'] == TestConstants.CV_PROJECT_END_DATE
        assert response_json['role'] == TestConstants.CV_PROJECT_ROLE
        assert response_json['link'] == TestConstants.CV_PROJECT_LINK
        assert response_json['description'] == TestConstants.CV_PROJECT_DESCRIPTION


#
