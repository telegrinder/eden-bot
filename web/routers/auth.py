from fastapi import APIRouter, Request, HTTPException, status
from web.responses.auth_info import AuthInfo
from client import api
from database.user import get_full
from web.jwt_token import JWTToken
import hmac
import json
import hashlib

router = APIRouter(tags=["auth"])


def webapp_validate_request(
    request: Request,
    bot_token: str,
) -> None:
    items = sorted(request.query_params.items(), key=lambda kv: kv[0])
    data_check_string = "\n".join(f"{k}={param}" for k, param in items if k != "hash")
    secret = hmac.new(
        "WebAppData".encode(), bot_token.encode(), hashlib.sha256
    ).digest()
    data_chk = hmac.new(secret, data_check_string.encode(), hashlib.sha256)

    is_valid = data_chk.hexdigest() == request.query_params.get("hash")
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid hash.",
        )


@router.post("/auth")
async def auth_handler(
    request: Request,
) -> AuthInfo:
    webapp_validate_request(request, api.token)
    user_id = json.loads(request.query_params.get("user"))["id"]

    user = await get_full(user_id)

    jwt = JWTToken.create_token(dict(user_id=str(user[0].id)), "access")
    return AuthInfo(token=jwt)
