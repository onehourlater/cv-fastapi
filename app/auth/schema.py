from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    email: str
    username: str


class UserBaseAuth(BaseModel):
    email: str
    password: str


class TokenType(BaseModel):
    token_type: str


class AccessToken(TokenType):
    access_token: str
    access_expires_seconds: int


class RefreshToken(TokenType):
    refresh_token: str
    refresh_expires_seconds: int


class AuthTokens(AccessToken, RefreshToken):
    pass
