import pydantic

class AuthInfo(pydantic.BaseModel):
    token: str
