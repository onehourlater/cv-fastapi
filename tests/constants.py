from sqlalchemy import Enum

class TestConstants(Enum):
    __test__ = False

    USER_EMAIL = 'hello@gmail.com'
    USER_PASSWORD = 'hellopassword'

    USER_PROFILE_DATA = {
        'full_name': 'Dmitry',
        'kind_of_activity': 'web delevoper',
        'about': 'about info',
    }
    CV_ABOUT = 'im web fullstack developer'

    CV_PROJECT_TITLE = 'Pingdog SAAS'
    CV_PROJECT_END_DATE = 1643662800
    CV_PROJECT_CLIENT = ''
    CV_PROJECT_LINK = 'https://pingdog.ru'
    CV_PROJECT_DESCRIPTION = 'Worked on realtime websites monitoring'
