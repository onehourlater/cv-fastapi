from decouple import config


class DBSettings:
    POSTGRES_HOSTNAME: str = config('DB_HOSTNAME', 'localhost')
    POSTGRES_DB: str = config('DB_NAME', '')
    POSTGRES_USER: str = config('DB_USER', '')
    POSTGRES_PASSWORD: str = config('DB_PASSWORD', '')
    DATABASE_PORT: int = config('DB_PORT', 5432)


class AuthSettings:
    JWT_SECRET: str = config('JWT_SECRET', '')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRES: int = config('JWT_EXPIRES', 300)  # 5 mins
    JWT_REFRESH_EXPIRES: int = config('JWT_REFRESH_EXPIRES', 2592000)  # 30 days
    JWT_USERNAME_KEY: int = 'fastusername'


db_settings = DBSettings()
auth_settings = AuthSettings()
