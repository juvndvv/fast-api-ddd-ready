from abc import ABC, abstractmethod

from fastapi import APIRouter


class Controller(ABC):
    @abstractmethod
    def get_router(self) -> APIRouter:
        """
        Método abstracto para obtener el router de la API.
        """
        pass
