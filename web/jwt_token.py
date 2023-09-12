import typing

from jose import jwt

from client import JWT_ALG, SECRET

TokenType = typing.Literal["access"]


class InvalidToken(Exception):
    pass


def parse_token(token: str) -> dict[str, typing.Any]:
    """Parses and validates token, returns payload"""
    try:
        return jwt.decode(
            token,
            SECRET,
            JWT_ALG,
        )
    except:
        raise InvalidToken


class JWTToken(str):
    @classmethod
    def create_token(cls, data: dict, token_type: TokenType) -> "JWTToken":
        token = jwt.encode(
            {
                **data,
                "token_type": token_type,
            },
            SECRET,
            JWT_ALG,
        )
        return cls(token)

    def validate_token(self, token_type: TokenType) -> dict:
        payload = parse_token(self)

        if payload.get("token_type") != token_type:
            raise InvalidToken

        return payload
