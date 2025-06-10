from abc import ABC, abstractmethod

from google.protobuf.message import Message


class GrpcRequest(ABC):
    """Clase abstracta para representar una petición gRPC."""

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Nombre del servicio gRPC."""
        pass

    @property
    @abstractmethod
    def method_name(self) -> str:
        """Nombre del método gRPC."""
        pass

    @property
    @abstractmethod
    def message(self) -> Message:
        """Mensaje protobuf a enviar."""
        pass

    @property
    @abstractmethod
    def metadata(self) -> dict[str, str]:
        """Metadatos de la petición."""
        pass

    @property
    @abstractmethod
    def timeout(self) -> float | None:
        """Timeout en segundos para la petición."""
        pass
