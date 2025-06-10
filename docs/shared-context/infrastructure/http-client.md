# HTTP Client - Infrastructure Layer

El **HTTP Client** proporciona una interfaz robusta y type-safe para realizar llamadas HTTP a servicios externos, con soporte para timeouts, reintentos, logging automático y correlación de traces.

## 🎯 Características

### **Funcionalidades Principales**
- ✅ **Type Safety**: Requests y responses fuertemente tipados
- ✅ **Context Manager**: Manejo automático de conexiones
- ✅ **Trace Correlation**: Propagación automática de trace_id
- ✅ **Error Handling**: Manejo robusto de errores HTTP
- ✅ **Timeouts**: Configuración flexible de timeouts
- ✅ **Logging**: Logging estructurado automático
- ✅ **Retries**: Reintentos automáticos con backoff
- ✅ **SSL/TLS**: Soporte completo para HTTPS

## 🏗️ Arquitectura

```
Infrastructure/Http/
├── Client/
│   ├── HttpClient.py           # Cliente HTTP principal
│   ├── HttpRequest.py          # Interfaz base para requests
│   ├── HttpResponse.py         # Response encapsulado
│   └── BaseHttpRequest.py      # Implementación base
├── Context/
│   ├── RequestContext.py       # Contexto de request
│   └── RequestContextMiddleware.py  # Middleware FastAPI
└── Controller.py               # Base controller
```

## 📚 Componentes

### **1. HttpClient**
Cliente principal para realizar llamadas HTTP.

```python
from app.Contexts.Shared.Infrastructure.Http.Client.HttpClient import HttpClient

# Uso básico con context manager
with HttpClient("https://api.example.com") as client:
    request = MyHttpRequest()
    response = client.send(request)
    
    if response.is_success():
        data = response.body()
        print(f"Success: {data}")
    else:
        print(f"Error: {response.status_code()} - {response.reason()}")
```

### **2. HttpRequest (Abstract)**
Interfaz base para definir requests HTTP.

```python
from app.Contexts.Shared.Infrastructure.Http.Client.HttpRequest import HttpRequest

class GetUserRequest(HttpRequest):
    def __init__(self, user_id: str):
        self._user_id = user_id
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return f"/users/{self._user_id}"
    
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def body(self) -> dict | None:
        return None  # GET no tiene body
    
    def timeout(self) -> int:
        return 30  # 30 segundos
```

### **3. BaseHttpRequest**
Implementación base con funcionalidades comunes.

```python
from app.Contexts.Shared.Infrastructure.Http.Client.BaseHttpRequest import BaseHttpRequest

class CreateUserRequest(BaseHttpRequest):
    def __init__(self, name: str, email: str, age: int):
        self._name = name
        self._email = email
        self._age = age
    
    def method(self) -> str:
        return "POST"
    
    def endpoint(self) -> str:
        return "/users"
    
    def body(self) -> dict:
        return {
            "name": self._name,
            "email": self._email,
            "age": self._age
        }
```

### **4. HttpResponse**
Encapsula la respuesta HTTP con métodos de conveniencia.

```python
from app.Contexts.Shared.Infrastructure.Http.Client.HttpResponse import HttpResponse

# El response se obtiene automáticamente del client
response = client.send(request)

# Métodos disponibles
print(f"Status: {response.status_code()}")        # 200
print(f"Success: {response.is_success()}")        # True
print(f"Headers: {response.headers()}")           # Dict[str, str]
print(f"Body: {response.body()}")                 # Dict | str | bytes
print(f"JSON: {response.json()}")                 # Para responses JSON
print(f"Text: {response.text()}")                 # Para responses de texto
```

## 💡 Ejemplos de Uso

### **1. GET Request Simple**
```python
class GetProductRequest(BaseHttpRequest):
    def __init__(self, product_id: str):
        self._product_id = product_id
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return f"/products/{self._product_id}"

# Uso
with HttpClient("https://api.store.com") as client:
    request = GetProductRequest("123")
    response = client.send(request)
    
    if response.is_success():
        product = response.json()
        print(f"Product: {product['name']} - ${product['price']}")
```

### **2. POST Request con Body**
```python
class CreateOrderRequest(BaseHttpRequest):
    def __init__(self, user_id: str, items: list[dict], total: float):
        self._user_id = user_id
        self._items = items
        self._total = total
    
    def method(self) -> str:
        return "POST"
    
    def endpoint(self) -> str:
        return "/orders"
    
    def body(self) -> dict:
        return {
            "user_id": self._user_id,
            "items": self._items,
            "total": self._total,
            "currency": "USD"
        }
    
    def headers(self) -> dict[str, str]:
        return {
            **super().headers(),
            "Idempotency-Key": str(uuid.uuid4())
        }

# Uso
with HttpClient("https://api.orders.com") as client:
    items = [
        {"product_id": "123", "quantity": 2, "price": 29.99},
        {"product_id": "456", "quantity": 1, "price": 49.99}
    ]
    
    request = CreateOrderRequest("user_789", items, 109.97)
    response = client.send(request)
    
    if response.is_success():
        order = response.json()
        print(f"Order created: {order['id']}")
    else:
        print(f"Error creating order: {response.status_code()}")
```

### **3. PUT Request para Actualización**
```python
class UpdateUserRequest(BaseHttpRequest):
    def __init__(self, user_id: str, name: str = None, email: str = None):
        self._user_id = user_id
        self._name = name
        self._email = email
    
    def method(self) -> str:
        return "PUT"
    
    def endpoint(self) -> str:
        return f"/users/{self._user_id}"
    
    def body(self) -> dict:
        body = {}
        if self._name:
            body["name"] = self._name
        if self._email:
            body["email"] = self._email
        return body

# Uso
with HttpClient("https://api.users.com") as client:
    request = UpdateUserRequest("123", name="John Updated")
    response = client.send(request)
    
    if response.is_success():
        user = response.json()
        print(f"User updated: {user['name']}")
```

### **4. Request con Autenticación**
```python
class AuthenticatedRequest(BaseHttpRequest):
    def __init__(self, token: str):
        self._token = token
    
    def headers(self) -> dict[str, str]:
        return {
            **super().headers(),
            "Authorization": f"Bearer {self._token}"
        }

class GetUserProfileRequest(AuthenticatedRequest):
    def __init__(self, token: str, user_id: str):
        super().__init__(token)
        self._user_id = user_id
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return f"/users/{self._user_id}/profile"

# Uso
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
with HttpClient("https://api.secure.com") as client:
    request = GetUserProfileRequest(token, "123")
    response = client.send(request)
```

## 🔧 Configuración Avanzada

### **1. Timeouts Personalizados**
```python
class SlowApiRequest(BaseHttpRequest):
    def timeout(self) -> int:
        return 120  # 2 minutos para APIs lentas
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return "/slow-operation"
```

### **2. Headers Personalizados**
```python
class CustomHeadersRequest(BaseHttpRequest):
    def headers(self) -> dict[str, str]:
        return {
            **super().headers(),
            "X-API-Version": "v2",
            "X-Client-ID": "yurest-app",
            "User-Agent": "Yurest/1.0",
            "Accept-Language": "es-ES,es;q=0.9"
        }
```

### **3. Request con Query Parameters**
```python
class SearchProductsRequest(BaseHttpRequest):
    def __init__(self, query: str, category: str = None, limit: int = 10):
        self._query = query
        self._category = category
        self._limit = limit
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        params = {"q": self._query, "limit": self._limit}
        if self._category:
            params["category"] = self._category
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"/products/search?{query_string}"
```

## 🔗 Integración con Request Context

### **Correlación Automática de Traces**
El HTTP Client integra automáticamente con `RequestContext` para propagar el `trace_id`:

```python
from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import RequestContext

# El trace_id se añade automáticamente a los headers
# No necesitas configurar nada adicional

class MyRequest(BaseHttpRequest):
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return "/api/data"

# Cuando se envía el request, automáticamente incluye:
# X-Trace-ID: <current_trace_id>
with HttpClient("https://api.example.com") as client:
    response = client.send(MyRequest())
```

### **Acceso Manual al Context**
```python
class CustomRequest(BaseHttpRequest):
    def headers(self) -> dict[str, str]:
        trace_id = RequestContext.get_trace_id()
        client_ip = RequestContext.get_client_ip()
        
        return {
            **super().headers(),
            "X-Trace-ID": trace_id,
            "X-Forwarded-For": client_ip,
            "X-Request-Source": "yurest-api"
        }
```

## 🧪 Testing

### **Mocking HTTP Calls**
```python
import pytest
from unittest.mock import Mock, patch
from app.Contexts.Shared.Infrastructure.Http.Client.HttpResponse import HttpResponse

class TestUserService:
    @patch('app.Contexts.Shared.Infrastructure.Http.Client.HttpClient.send')
    def test_get_user_success(self, mock_send):
        # Arrange
        mock_response = Mock(spec=HttpResponse)
        mock_response.is_success.return_value = True
        mock_response.json.return_value = {
            "id": "123",
            "name": "John Doe",
            "email": "john@example.com"
        }
        mock_send.return_value = mock_response
        
        service = UserService()
        
        # Act
        user = service.get_user("123")
        
        # Assert
        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
        mock_send.assert_called_once()
    
    @patch('app.Contexts.Shared.Infrastructure.Http.Client.HttpClient.send')
    def test_get_user_not_found(self, mock_send):
        # Arrange
        mock_response = Mock(spec=HttpResponse)
        mock_response.is_success.return_value = False
        mock_response.status_code.return_value = 404
        mock_send.return_value = mock_response
        
        service = UserService()
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            service.get_user("999")
```

### **Integration Tests**
```python
class TestHttpClientIntegration:
    def test_real_api_call(self):
        # Para tests de integración con APIs reales
        with HttpClient("https://jsonplaceholder.typicode.com") as client:
            request = GetPostRequest("1")
            response = client.send(request)
            
            assert response.is_success()
            post = response.json()
            assert "title" in post
            assert "body" in post
```

## 🚀 Uso en Services

### **Service Layer Pattern**
```python
class ExternalUserService:
    def __init__(self, base_url: str, api_key: str):
        self._base_url = base_url
        self._api_key = api_key
    
    def get_user(self, user_id: str) -> dict:
        with HttpClient(self._base_url) as client:
            request = GetUserRequest(user_id, self._api_key)
            response = client.send(request)
            
            if response.is_success():
                return response.json()
            elif response.status_code() == 404:
                raise UserNotFoundError(f"User {user_id} not found")
            else:
                raise ExternalServiceError(
                    f"Failed to get user: {response.status_code()}"
                )
    
    def create_user(self, user_data: dict) -> str:
        with HttpClient(self._base_url) as client:
            request = CreateUserRequest(user_data, self._api_key)
            response = client.send(request)
            
            if response.is_success():
                return response.json()["id"]
            else:
                raise ExternalServiceError(
                    f"Failed to create user: {response.status_code()}"
                )

class GetUserRequest(BaseHttpRequest):
    def __init__(self, user_id: str, api_key: str):
        self._user_id = user_id
        self._api_key = api_key
    
    def method(self) -> str:
        return "GET"
    
    def endpoint(self) -> str:
        return f"/users/{self._user_id}"
    
    def headers(self) -> dict[str, str]:
        return {
            **super().headers(),
            "X-API-Key": self._api_key
        }
```

### **Dependency Injection**
```python
# En tu módulo de DI
class ExternalServicesModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ExternalUserService).to_instance(
            ExternalUserService(
                base_url="https://api.external.com",
                api_key=os.getenv("EXTERNAL_API_KEY")
            )
        )

# En tu handler
class CreateUserCommandHandler(CommandHandler):
    def __init__(self, external_service: ExternalUserService):
        self._external_service = external_service
    
    def handle(self, command: CreateUserCommand) -> None:
        try:
            external_id = self._external_service.create_user({
                "name": command.name,
                "email": command.email
            })
            
            # Continuar con lógica local...
            
        except ExternalServiceError as e:
            logger.error(f"External service failed: {e}")
            # Manejar error apropiadamente
```

El HTTP Client proporciona una base sólida para integrar con servicios externos de manera robusta y mantenible, con logging automático y correlación de traces para facilitar el debugging y monitoreo. 