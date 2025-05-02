import pytest
from datetime import datetime
from unittest import TestCase

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from sqlalchemy import select
from sqlalchemy.orm import Session

from tests.constants import TestConstants
from tests.factories.user import UserFactory
from tests.factories.cv import CVFactory

from app.config import auth_settings

from app.user.models import User
from app.auth.manager import get_auth_manager, get_current_user
from app.auth.utils import create_JWT_token
from app.auth import utils as auth_utils
from app.auth import schema as auth_schema


@pytest.mark.usefixtures('client')
class TestCVProject:
    def test_get_cv_projects(self, authenticated_client: TestClient, default_user: User, auth_manager):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.get(f'/api/v1/cvs/{cv.id}/projects')
        assert response.status_code == 200
        response_json = response.json()

    def test_get_cv_projects_no_permissions(self, authenticated_client: TestClient, default_user: User, auth_manager):
        cv: CV = CVFactory()

        response = authenticated_client.get(f'/api/v1/cvs/{cv.id}/projects')
        assert response.status_code == 403
        response_json = response.json()

    def test_create_cv_project(self, authenticated_client: TestClient, default_user: User, auth_manager):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.post(f'/api/v1/cvs/{cv.id}/projects', json={
            'title': TestConstants.CV_PROJECT_TITLE,
            'end_date': TestConstants.CV_PROJECT_END_DATE,
            'client': TestConstants.CV_PROJECT_CLIENT,
            'link': TestConstants.CV_PROJECT_LINK,
            'description': TestConstants.CV_PROJECT_DESCRIPTION,
        })
        assert response.status_code == 200
        response_json = response.json()
        print()
        print('response_json: ', response_json)
        assert response_json['title'] == TestConstants.CV_PROJECT_TITLE
        assert response_json['end_date'] == datetime.utcfromtimestamp(TestConstants.CV_PROJECT_END_DATE).strftime('%Y-%m-%dT%H:%M:%S')
        assert response_json['client'] == TestConstants.CV_PROJECT_CLIENT
        assert response_json['link'] == TestConstants.CV_PROJECT_LINK
        assert response_json['description'] == TestConstants.CV_PROJECT_DESCRIPTION







#
