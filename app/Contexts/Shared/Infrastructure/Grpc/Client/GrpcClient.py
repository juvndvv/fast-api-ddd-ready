import logging
from typing import Any

import grpc

from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcRequest import GrpcRequest
from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcResponse import GrpcResponse
from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import (
    RequestContext,
)


class GrpcClient:
    """Cliente gRPC con manejo de conexiones y contexto de request."""

    def __init__(
        self,
        server_address: str,
        timeout: float = 30.0,
        max_receive_message_length: int = 4 * 1024 * 1024,  # 4MB
        max_send_message_length: int = 4 * 1024 * 1024,  # 4MB
        compression: grpc.Compression | None = None,
    ):
        self._server_address = server_address
        self._timeout = timeout
        self._logger = logging.getLogger(__name__)

        # Opciones del canal
        self._channel_options = [
            ("grpc.max_receive_message_length", max_receive_message_length),
            ("grpc.max_send_message_length", max_send_message_length),
        ]

        self._compression = compression
        self._channel: grpc.Channel | None = None

    def _get_channel(self) -> grpc.Channel:
        """Obtiene o crea el canal gRPC."""
        if self._channel is None:
            self._channel = grpc.insecure_channel(
                self._server_address, options=self._channel_options
            )
        return self._channel

    def _prepare_metadata(self, request: GrpcRequest) -> list[tuple[str, str]]:
        """Prepara los metadatos incluyendo el trace_id del contexto."""
        metadata = dict(request.metadata)

        # Agregar trace_id del contexto actual si existe
        trace_id = RequestContext.get_trace_id()
        if trace_id:
            metadata["x-trace-id"] = trace_id

        # Convertir a lista de tuplas como espera gRPC
        return list(metadata.items())

    def send(self, request: GrpcRequest, stub_class: type[Any]) -> GrpcResponse:
        """
        Envía una petición gRPC síncrona.

        Args:
            request: La petición gRPC a enviar
            stub_class: Clase del stub generado por protobuf

        Returns:
            GrpcResponse: La respuesta gRPC recibida
        """
        try:
            channel = self._get_channel()
            stub = stub_class(channel)

            # Preparar metadatos
            metadata = self._prepare_metadata(request)

            # Obtener timeout
            timeout = request.timeout or self._timeout

            # Log de inicio
            self._logger.info(
                f"gRPC call started: {request.service_name}.{request.method_name} to {self._server_address}"
            )

            # Realizar la llamada gRPC
            method = getattr(stub, request.method_name)
            response_message = method(
                request.message,
                timeout=timeout,
                metadata=metadata,
                compression=self._compression,
            )

            self._logger.info(
                f"gRPC call completed: {request.service_name}.{request.method_name}"
            )

            return GrpcResponse(
                message=response_message,
                metadata={},  # Los metadatos de respuesta requieren llamadas con interceptors
                status_code=grpc.StatusCode.OK,
            )

        except grpc.RpcError as e:
            self._logger.error(
                f"gRPC call failed: {request.service_name}.{request.method_name} - {e.code().name}: {e.details()}",
                exc_info=e,
            )

            return GrpcResponse(
                message=None, metadata={}, status_code=e.code(), details=e.details()
            )

        except Exception as e:
            self._logger.error(
                f"Unexpected error in gRPC call: {request.service_name}.{request.method_name} - {str(e)}",
                exc_info=e,
            )

            return GrpcResponse(
                message=None,
                metadata={},
                status_code=grpc.StatusCode.INTERNAL,
                details=str(e),
            )

    async def send_async(
        self, request: GrpcRequest, stub_class: type[Any]
    ) -> GrpcResponse:
        """
        Envía una petición gRPC asíncrona.

        Args:
            request: La petición gRPC a enviar
            stub_class: Clase del stub generado por protobuf

        Returns:
            GrpcResponse: La respuesta gRPC recibida
        """
        try:
            channel = grpc.aio.insecure_channel(
                self._server_address, options=self._channel_options
            )

            stub = stub_class(channel)

            # Preparar metadatos
            metadata = self._prepare_metadata(request)

            # Obtener timeout
            timeout = request.timeout or self._timeout

            # Log de inicio
            self._logger.info(
                f"Async gRPC call started: {request.service_name}.{request.method_name} to {self._server_address}"
            )

            # Realizar la llamada gRPC asíncrona
            method = getattr(stub, request.method_name)
            response_message = await method(
                request.message,
                timeout=timeout,
                metadata=metadata,
                compression=self._compression,
            )

            self._logger.info(
                f"Async gRPC call completed: {request.service_name}.{request.method_name}"
            )

            await channel.close()

            return GrpcResponse(
                message=response_message, metadata={}, status_code=grpc.StatusCode.OK
            )

        except grpc.RpcError as e:
            self._logger.error(
                f"Async gRPC call failed: {request.service_name}.{request.method_name} - {e.code().name}: {e.details()}",
                exc_info=e,
            )

            return GrpcResponse(
                message=None, metadata={}, status_code=e.code(), details=e.details()
            )

        except Exception as e:
            self._logger.error(
                f"Unexpected error in async gRPC call: {request.service_name}.{request.method_name} - {str(e)}",
                exc_info=e,
            )

            return GrpcResponse(
                message=None,
                metadata={},
                status_code=grpc.StatusCode.INTERNAL,
                details=str(e),
            )

    def close(self) -> None:
        """Cierra la conexión gRPC."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._logger.info(f"gRPC connection closed: {self._server_address}")

    def __enter__(self) -> "GrpcClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
