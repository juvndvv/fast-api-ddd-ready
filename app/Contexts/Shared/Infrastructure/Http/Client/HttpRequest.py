from abc import ABC, abstractmethod

from app.Contexts.Shared.Infrastructure.Http.Client.HttpMethod import HttpMethod


class HttpRequest(ABC):
    @property
    @abstractmethod
    def method(self) -> HttpMethod:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def body(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def query_params(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def content_type(self) -> str:
        pass

    @property
    @abstractmethod
    def files(self) -> dict[str, bytes]:
        pass
