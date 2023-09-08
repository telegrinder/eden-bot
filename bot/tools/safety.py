import re
import typing


def remove_links(s: str) -> str:
    # todo remove short urls
    return re.sub(r"http\S+", "", s)


def make_safe(s: typing.Optional[str]) -> str:
    if not s:
        return ""
    return remove_links(s)
