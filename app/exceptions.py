class AppException(Exception):
    pass

class ExistsError(ValueError):
    code = 'exists'
    msg_template = '{msg}'

class NotExistsError(ValueError):
    code = 'not-exists'
    msg_template = '{msg}'

class WrongCredentials(ValueError):
    code = 'wrong-credentials'
    msg_template = '{msg}'

class NoPermission(AppException):
    code = 'no-permission'
    msg_template = '{msg}'
