import factory

from tests.constants import TestConstants

from app.user.models import User
from app.auth.utils import get_password_hash


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = 'commit'

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.LazyFunction(
        lambda: get_password_hash(TestConstants.USER_PASSWORD)
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        print()
        print('_create')
        if 'v' in kwargs:
            kwargs['password'] = get_password_hash(kwargs.pop('password'))
        return super()._create(model_class, *args, **kwargs)
