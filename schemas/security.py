from pydantic import BaseModel


class AuthToken(BaseModel):
    authToken: str


class AccessToken(BaseModel):
    access_token: str
    expires: int


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
