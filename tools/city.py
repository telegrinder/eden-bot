import typing
import aiofiles


async def search_city(name: str) -> typing.Optional[int]:
    name = name.lower().strip(" ").replace(" ", "")
    async with aiofiles.open("CITIES") as stream:
        async for line in stream:
            s = str(line).strip("\n")
            i, names = s.split(":")
            names = list(map(lambda x: x.replace(" ", ""), names.split(" | ")))
            if name in names:
                return int(i)
    return None
