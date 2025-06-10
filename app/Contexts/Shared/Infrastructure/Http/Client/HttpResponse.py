from typing import Any


class HttpResponse:
    __slots__ = ("_status_code", "_body", "_content_type", "_headers")

    def __init__(
        self, status_code: int, body: Any, content_type: str, headers: dict[str, str]
    ):
        self._status_code = status_code
        self._body = body
        self._content_type = content_type
