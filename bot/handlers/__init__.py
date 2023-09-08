import telegrinder
import typing

from . import start, profile, feed, like, requests, reset, settings, admin, report

dps: typing.Iterable["telegrinder.Dispatch"] = (
    feed.dp,
    profile.dp,
    like.dp,
    report.dp,
    requests.dp,
    start.dp,
    settings.dp,
    reset.dp,
    admin.dp,
)
