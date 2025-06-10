from abc import ABC, abstractmethod

from fastapi import Request
from starlette.responses import JSONResponse


class ExceptionHandler(ABC):
    @abstractmethod
    async def handle(self, request: Request, exc: Exception) -> JSONResponse:
        pass
