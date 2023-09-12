from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, status, HTTPException
from web.jwt_token import JWTToken, InvalidToken
from database.user import get_by_uid, User

security = HTTPBearer()


async def get_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials
    try:
        validation = JWTToken(token).validate_token(token_type="access")
        user_id = validation["user_id"]
        user = await get_by_uid(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User undefined."
            )
        return user[0]
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
