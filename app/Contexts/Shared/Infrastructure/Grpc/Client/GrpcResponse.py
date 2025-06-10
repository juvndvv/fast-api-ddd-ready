import grpc
from google.protobuf.message import Message


class GrpcResponse:
    """Representa una respuesta gRPC."""

    __slots__ = ("_message", "_metadata", "_status_code", "_details")

    def __init__(
        self,
        message: Message | None = None,
        metadata: dict[str, str] | None = None,
        status_code: grpc.StatusCode = grpc.StatusCode.OK,
        details: str | None = None,
    ):
        self._message = message
        self._metadata = metadata or {}
        self._status_code = status_code
        self._details = details

    @property
    def message(self) -> Message | None:
        """Mensaje protobuf de respuesta."""
        return self._message

    @property
    def metadata(self) -> dict[str, str]:
        """Metadatos de la respuesta."""
        return self._metadata

    @property
    def status_code(self) -> grpc.StatusCode:
        """Código de estado gRPC."""
        return self._status_code

    @property
    def details(self) -> str | None:
        """Detalles del error si existe."""
        return self._details

    @property
    def is_success(self) -> bool:
        """Indica si la respuesta fue exitosa."""
        return bool(self._status_code == grpc.StatusCode.OK)

    def __str__(self) -> str:
        return f"GrpcResponse(status={self._status_code.name}, message={self._message})"
