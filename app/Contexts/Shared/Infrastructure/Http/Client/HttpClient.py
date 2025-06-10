from typing import Any

import httpx

from app.Contexts.Shared.Infrastructure.Http.Client.HttpRequest import HttpRequest
from app.Contexts.Shared.Infrastructure.Http.Client.HttpResponse import HttpResponse


class HttpClient:
    def __init__(self, base_url: str = "", timeout: float = 30.0):
        self._base_url = base_url
        self._timeout = timeout
        self._client = httpx.Client(
            base_url=base_url, timeout=timeout, follow_redirects=True
        )

    def send(self, request: HttpRequest) -> HttpResponse:
        """
        Envía una petición HTTP y devuelve la respuesta.

        Args:
            request: La petición HTTP a enviar

        Returns:
            HttpResponse: La respuesta HTTP recibida
        """
        try:
            response = self._client.request(
                method=request.method.value,
                url=request.url,
                headers=request.headers,
                params=request.query_params,
                json=(
                    request.body if request.content_type == "application/json" else None
                ),
                data=(
                    request.body if request.content_type != "application/json" else None
                ),
                files=request.files,
            )

            return HttpResponse(
                status_code=response.status_code,
                body=response.content,
                content_type=response.headers.get("content-type", "application/json"),
                headers=dict(response.headers),
            )

        except httpx.TimeoutException as e:
            raise TimeoutError(
                f"La petición ha excedido el tiempo límite de {self._timeout} segundos"
            ) from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Error al realizar la petición: {str(e)}") from e
        except Exception as e:
            raise Exception(
                f"Error inesperado al realizar la petición: {str(e)}"
            ) from e

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._client.close()
