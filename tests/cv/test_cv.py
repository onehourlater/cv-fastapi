import pytest
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
class TestCV:
    def test_create_cv(self, authenticated_client: TestClient, auth_manager):
        response = authenticated_client.post(f'/api/v1/cvs/', json={
            'about': TestConstants.CV_ABOUT,
        })
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['about'] == TestConstants.CV_ABOUT

    def test_get_cvs(self, authenticated_client: TestClient, default_user: User, auth_manager):
        cv: CV = CVFactory(user=default_user)

        response = authenticated_client.get(f'/api/v1/cvs/')
        assert response.status_code == 200
        response_json = response.json()
        response_json_cv = response_json[0]
        assert response_json_cv['about'] == cv.about






#
