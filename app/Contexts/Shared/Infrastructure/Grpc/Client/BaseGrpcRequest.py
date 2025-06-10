from google.protobuf.message import Message

from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcRequest import GrpcRequest


class BaseGrpcRequest(GrpcRequest):
    """Implementación base de GrpcRequest para facilitar la creación de peticiones concretas."""

    def __init__(
        self,
        service_name: str,
        method_name: str,
        message: Message,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ):
        self._service_name = service_name
        self._method_name = method_name
        self._message = message
        self._metadata = metadata or {}
        self._timeout = timeout

    @property
    def service_name(self) -> str:
        return self._service_name

    @property
    def method_name(self) -> str:
        return self._method_name

    @property
    def message(self) -> Message:
        return self._message

    @property
    def metadata(self) -> dict[str, str]:
        return self._metadata

    @property
    def timeout(self) -> float | None:
        return self._timeout
