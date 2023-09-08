from fastapi import APIRouter, Response, HTTPException, status
import pydantic
from database import uni
from web.dependencies import get_auth, Depends, User

router = APIRouter(prefix="/uni")


class University(pydantic.BaseModel):
    id: str
    city_id: int
    name: str


@router.get("/search")
async def uni_search_handler(q: str | None = None) -> list[University]:
    if q == "":
        return []
    return [
        University(id=str(university.id), name=university.name, city_id=university.city)
        for university in await uni.search(q)
    ]


@router.put("/")
async def set_uni_handler(uni_id: str, user: User = Depends(get_auth)) -> Response:
    try:
        await uni.set_uni(user.telegram_id, uni_id)
    except:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid university id.")
    return Response(status_code=200)


@router.delete("/")
async def unset_uni_handler(user: User = Depends(get_auth)) -> Response:
    await uni.set_uni(user.telegram_id, None)
    return Response(status_code=200)
