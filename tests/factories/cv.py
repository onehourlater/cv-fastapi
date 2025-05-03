import factory

from tests.factories.user import UserFactory

from app.cv.models import CV, PublicStatus


class CVFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CV
        sqlalchemy_session_persistence = 'commit'

    about = factory.Faker('job')
    user = factory.SubFactory(UserFactory)
    # TODO: it it possible to depends on database records?
    position = factory.Faker('pyint', min_value=1, max_value=1000)

    public_status = PublicStatus.PRIVATE


    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        print()
        print('[CVFactory] _create')
        return super()._create(model_class, *args, **kwargs)
