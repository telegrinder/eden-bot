from fastapi import APIRouter
import pydantic
from bot.tools.city import list_cities

router = APIRouter(prefix="/data")


class City(pydantic.BaseModel):
    id: int
    name: str


@router.get("/city_lst")
async def uni_search_handler() -> list[City]:
    return [
        City(id=k, name=v)
        for k, v in (await list_cities()).items()
    ]
