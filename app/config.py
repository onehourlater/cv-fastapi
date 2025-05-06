from decouple import config


class AppSettings:
    MEDIA_FOLDER_PATH: str = config('MEDIA_FOLDER_PATH', None)
    CV_SLUG_PATTERN: str = '^[A-Za-z0-9_-]*$'


class DBSettings:
    POSTGRES_HOSTNAME: str = config('POSTGRES_HOSTNAME', 'localhost')
    POSTGRES_DB: str = config('POSTGRES_DB', '')
    POSTGRES_USER: str = config('POSTGRES_USER', '')
    POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD', '')
    DATABASE_PORT: int = config('POSTGRES_PORT', 5432)


class AuthSettings:
    JWT_SECRET: str = config('JWT_SECRET', '')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRES: int = config('JWT_EXPIRES', 300)  # 5 mins
    JWT_REFRESH_EXPIRES: int = config('JWT_REFRESH_EXPIRES', 2592000)  # 30 days
    JWT_USERNAME_KEY: int = 'fastusername'


db_settings = DBSettings()
auth_settings = AuthSettings()
