# gRPC Client - Infrastructure Layer

El **gRPC Client** proporciona una interfaz type-safe para comunicación con servicios gRPC, con soporte para metadata, timeouts, manejo de errores, correlación de traces y métodos síncronos/asíncronos.

## 🎯 Características

### **Funcionalidades Principales**
- ✅ **Type Safety**: Requests y responses fuertemente tipados con protobuf
- ✅ **Sync/Async**: Soporte para llamadas síncronas y asíncronas
- ✅ **Trace Correlation**: Propagación automática de trace_id en metadata
- ✅ **Error Handling**: Manejo robusto de errores gRPC
- ✅ **Timeouts**: Configuración flexible por request
- ✅ **Metadata**: Soporte completo para headers/metadata gRPC
- ✅ **Connection Management**: Pooling y reutilización de conexiones
- ✅ **Logging**: Logging estructurado automático

## 🏗️ Arquitectura

```
Infrastructure/Grpc/
└── Client/
    ├── GrpcClient.py           # Cliente gRPC principal
    ├── GrpcRequest.py          # Interfaz base para requests
    ├── GrpcResponse.py         # Response encapsulado
    └── BaseGrpcRequest.py      # Implementación base
```

## 📚 Componentes

### **1. GrpcClient**
Cliente principal para realizar llamadas gRPC.

```python
from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcClient import GrpcClient

# Configuración básica
client = GrpcClient("localhost:50051")

# Llamada síncrona
request = GetUserGrpcRequest(user_id="123")
response = client.call(request)

if response.is_success():
    user = response.message()
    print(f"User: {user.name}")

# Llamada asíncrona
response = await client.call_async(request)

# Cleanup
client.close()
```

### **2. GrpcRequest (Abstract)**
Interfaz base para definir requests gRPC.

```python
from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcRequest import GrpcRequest

class GetUserGrpcRequest(GrpcRequest):
    def __init__(self, user_id: str):
        self._user_id = user_id
    
    def service_name(self) -> str:
        return "user.UserService"
    
    def method_name(self) -> str:
        return "GetUser"
    
    def message(self) -> Any:
        # Crear mensaje protobuf
        from protos.user_pb2 import GetUserRequest
        return GetUserRequest(user_id=self._user_id)
    
    def metadata(self) -> dict[str, str]:
        return {
            "authorization": "Bearer <token>",
            "x-client-version": "1.0"
        }
    
    def timeout(self) -> float:
        return 30.0  # 30 segundos
```

### **3. BaseGrpcRequest**
Implementación base con funcionalidades comunes.

```python
from app.Contexts.Shared.Infrastructure.Grpc.Client.BaseGrpcRequest import BaseGrpcRequest

class CreateUserGrpcRequest(BaseGrpcRequest):
    def __init__(self, name: str, email: str, age: int):
        self._name = name
        self._email = email
        self._age = age
    
    def service_name(self) -> str:
        return "user.UserService"
    
    def method_name(self) -> str:
        return "CreateUser"
    
    def message(self) -> Any:
        from protos.user_pb2 import CreateUserRequest
        return CreateUserRequest(
            name=self._name,
            email=self._email,
            age=self._age
        )
```

### **4. GrpcResponse**
Encapsula la respuesta gRPC con métodos de conveniencia.

```python
from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcResponse import GrpcResponse

# El response se obtiene automáticamente del client
response = client.call(request)

# Métodos disponibles
print(f"Success: {response.is_success()}")          # True/False
print(f"Status: {response.status_code()}")          # grpc.StatusCode
print(f"Details: {response.details()}")             # Error details
print(f"Metadata: {response.metadata()}")           # Response metadata
print(f"Message: {response.message()}")             # Protobuf message
```

## 💡 Ejemplos de Uso

### **1. Get Request Simple**
```python
# Definir el protobuf request
class GetProductGrpcRequest(BaseGrpcRequest):
    def __init__(self, product_id: str):
        self._product_id = product_id
    
    def service_name(self) -> str:
        return "catalog.ProductService"
    
    def method_name(self) -> str:
        return "GetProduct"
    
    def message(self) -> Any:
        from protos.catalog_pb2 import GetProductRequest
        return GetProductRequest(product_id=self._product_id)

# Uso
client = GrpcClient("catalog-service:50051")
try:
    request = GetProductGrpcRequest("prod_123")
    response = client.call(request)
    
    if response.is_success():
        product = response.message()
        print(f"Product: {product.name} - ${product.price}")
    else:
        print(f"Error: {response.status_code()} - {response.details()}")
finally:
    client.close()
```

### **2. Create Request con Autenticación**
```python
class CreateOrderGrpcRequest(BaseGrpcRequest):
    def __init__(self, user_id: str, items: list, total: float, token: str):
        self._user_id = user_id
        self._items = items
        self._total = total
        self._token = token
    
    def service_name(self) -> str:
        return "order.OrderService"
    
    def method_name(self) -> str:
        return "CreateOrder"
    
    def message(self) -> Any:
        from protos.order_pb2 import CreateOrderRequest, OrderItem
        
        order_items = [
            OrderItem(product_id=item["product_id"], 
                     quantity=item["quantity"],
                     price=item["price"])
            for item in self._items
        ]
        
        return CreateOrderRequest(
            user_id=self._user_id,
            items=order_items,
            total=self._total
        )
    
    def metadata(self) -> dict[str, str]:
        return {
            **super().metadata(),
            "authorization": f"Bearer {self._token}",
            "idempotency-key": str(uuid.uuid4())
        }
    
    def timeout(self) -> float:
        return 60.0  # Operaciones de orden pueden tardar más

# Uso
client = GrpcClient("order-service:50051")
try:
    items = [
        {"product_id": "prod_123", "quantity": 2, "price": 29.99},
        {"product_id": "prod_456", "quantity": 1, "price": 49.99}
    ]
    
    request = CreateOrderGrpcRequest(
        user_id="user_789",
        items=items,
        total=109.97,
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    response = client.call(request)
    
    if response.is_success():
        order = response.message()
        print(f"Order created: {order.order_id}")
    else:
        print(f"Failed to create order: {response.details()}")
finally:
    client.close()
```

### **3. Request Asíncrono**
```python
import asyncio

class SearchProductsGrpcRequest(BaseGrpcRequest):
    def __init__(self, query: str, limit: int = 10):
        self._query = query
        self._limit = limit
    
    def service_name(self) -> str:
        return "search.SearchService"
    
    def method_name(self) -> str:
        return "SearchProducts"
    
    def message(self) -> Any:
        from protos.search_pb2 import SearchRequest
        return SearchRequest(query=self._query, limit=self._limit)

async def search_products(query: str):
    client = GrpcClient("search-service:50051")
    try:
        request = SearchProductsGrpcRequest(query)
        response = await client.call_async(request)
        
        if response.is_success():
            search_results = response.message()
            return [
                {"id": result.id, "name": result.name, "price": result.price}
                for result in search_results.products
            ]
        else:
            raise SearchError(f"Search failed: {response.details()}")
    finally:
        client.close()

# Uso
results = asyncio.run(search_products("laptop"))
print(f"Found {len(results)} products")
```

### **4. Request con Metadata Personalizado**
```python
class AdminRequest(BaseGrpcRequest):
    def __init__(self, admin_token: str):
        self._admin_token = admin_token
    
    def metadata(self) -> dict[str, str]:
        return {
            **super().metadata(),
            "authorization": f"Bearer {self._admin_token}",
            "x-admin-action": "true",
            "x-request-source": "admin-panel"
        }

class GetUserStatisticsGrpcRequest(AdminRequest):
    def __init__(self, admin_token: str, start_date: str, end_date: str):
        super().__init__(admin_token)
        self._start_date = start_date
        self._end_date = end_date
    
    def service_name(self) -> str:
        return "analytics.AnalyticsService"
    
    def method_name(self) -> str:
        return "GetUserStatistics"
    
    def message(self) -> Any:
        from protos.analytics_pb2 import StatisticsRequest
        return StatisticsRequest(
            start_date=self._start_date,
            end_date=self._end_date
        )
    
    def timeout(self) -> float:
        return 120.0  # Analytics pueden tardar más
```

## 🔧 Configuración Avanzada

### **1. Cliente con Pool de Conexiones**
```python
class PooledGrpcService:
    def __init__(self, service_url: str, max_connections: int = 10):
        self._service_url = service_url
        self._clients = []
        self._max_connections = max_connections
        self._current = 0
    
    def get_client(self) -> GrpcClient:
        if len(self._clients) < self._max_connections:
            client = GrpcClient(self._service_url)
            self._clients.append(client)
            return client
        
        # Round robin
        client = self._clients[self._current]
        self._current = (self._current + 1) % len(self._clients)
        return client
    
    def close_all(self):
        for client in self._clients:
            client.close()
        self._clients.clear()
```

### **2. Request con Retry Logic**
```python
import time
from typing import Optional

class RetryableGrpcRequest(BaseGrpcRequest):
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
    
    def execute_with_retry(self, client: GrpcClient) -> GrpcResponse:
        last_error = None
        
        for attempt in range(self._max_retries + 1):
            try:
                response = client.call(self)
                
                if response.is_success():
                    return response
                
                # No retry for client errors (4xx equivalent)
                if response.status_code() in [grpc.StatusCode.INVALID_ARGUMENT, 
                                            grpc.StatusCode.NOT_FOUND]:
                    return response
                
                last_error = response
                
            except Exception as e:
                last_error = e
            
            if attempt < self._max_retries:
                wait_time = self._backoff_factor ** attempt
                time.sleep(wait_time)
        
        if isinstance(last_error, GrpcResponse):
            return last_error
        else:
            raise last_error
```

### **3. Service Discovery Integration**
```python
class ServiceDiscoveryGrpcClient:
    def __init__(self, service_registry: ServiceRegistry):
        self._service_registry = service_registry
        self._clients: dict[str, GrpcClient] = {}
    
    def get_client(self, service_name: str) -> GrpcClient:
        if service_name not in self._clients:
            service_url = self._service_registry.discover(service_name)
            self._clients[service_name] = GrpcClient(service_url)
        
        return self._clients[service_name]
    
    def call_service(self, service_name: str, request: GrpcRequest) -> GrpcResponse:
        client = self.get_client(service_name)
        return client.call(request)
```

## 🔗 Integración con Request Context

### **Correlación Automática de Traces**
El gRPC Client integra automáticamente con `RequestContext`:

```python
from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import RequestContext

class MyGrpcRequest(BaseGrpcRequest):
    def service_name(self) -> str:
        return "my.Service"
    
    def method_name(self) -> str:
        return "MyMethod"
    
    def message(self) -> Any:
        from protos.my_pb2 import MyRequest
        return MyRequest()

# El trace_id se propaga automáticamente en metadata
# No necesitas configurar nada adicional
client = GrpcClient("service:50051")
response = client.call(MyGrpcRequest())
```

### **Metadata Personalizado con Context**
```python
class ContextAwareGrpcRequest(BaseGrpcRequest):
    def metadata(self) -> dict[str, str]:
        trace_id = RequestContext.get_trace_id()
        client_ip = RequestContext.get_client_ip()
        
        return {
            **super().metadata(),
            "x-trace-id": trace_id,
            "x-client-ip": client_ip,
            "x-request-source": "yurest-api"
        }
```

## 🧪 Testing

### **Mocking gRPC Calls**
```python
import pytest
from unittest.mock import Mock, patch
from app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcResponse import GrpcResponse

class TestUserService:
    @patch('app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcClient.call')
    def test_get_user_success(self, mock_call):
        # Arrange
        from protos.user_pb2 import User
        user_proto = User(id="123", name="John Doe", email="john@example.com")
        
        mock_response = Mock(spec=GrpcResponse)
        mock_response.is_success.return_value = True
        mock_response.message.return_value = user_proto
        mock_call.return_value = mock_response
        
        service = UserGrpcService()
        
        # Act
        user = service.get_user("123")
        
        # Assert
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        mock_call.assert_called_once()
    
    @patch('app.Contexts.Shared.Infrastructure.Grpc.Client.GrpcClient.call')
    def test_get_user_not_found(self, mock_call):
        # Arrange
        mock_response = Mock(spec=GrpcResponse)
        mock_response.is_success.return_value = False
        mock_response.status_code.return_value = grpc.StatusCode.NOT_FOUND
        mock_response.details.return_value = "User not found"
        mock_call.return_value = mock_response
        
        service = UserGrpcService()
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            service.get_user("999")
```

### **Integration Tests con Test Server**
```python
import grpc
from grpc_testing import server_from_dictionary

class TestGrpcClientIntegration:
    def test_real_grpc_call(self):
        # Setup test server
        test_server = server_from_dictionary({
            "user.UserService": UserServiceImpl()
        }, grpc.server(thread_pool=None))
        
        # Test client
        client = GrpcClient("localhost:50051")
        try:
            request = GetUserGrpcRequest("123")
            response = client.call(request)
            
            assert response.is_success()
            user = response.message()
            assert user.id == "123"
        finally:
            client.close()
```

## 🚀 Uso en Services

### **Service Layer Pattern**
```python
class UserGrpcService:
    def __init__(self, grpc_client: GrpcClient):
        self._client = grpc_client
    
    def get_user(self, user_id: str) -> dict:
        request = GetUserGrpcRequest(user_id)
        response = self._client.call(request)
        
        if response.is_success():
            user = response.message()
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at
            }
        elif response.status_code() == grpc.StatusCode.NOT_FOUND:
            raise UserNotFoundError(f"User {user_id} not found")
        else:
            raise GrpcServiceError(
                f"Failed to get user: {response.details()}"
            )
    
    def create_user(self, user_data: dict) -> str:
        request = CreateUserGrpcRequest(**user_data)
        response = self._client.call(request)
        
        if response.is_success():
            user = response.message()
            return user.id
        else:
            raise GrpcServiceError(
                f"Failed to create user: {response.details()}"
            )
    
    def close(self):
        self._client.close()
```

### **Dependency Injection**
```python
# En tu módulo de DI
class GrpcServicesModule(Module):
    def configure(self, binder: Binder) -> None:
        # Cliente gRPC para User Service
        user_client = GrpcClient(os.getenv("USER_SERVICE_URL", "user-service:50051"))
        binder.bind(GrpcClient, annotation="user_service").to_instance(user_client)
        
        # Service que usa el cliente
        binder.bind(UserGrpcService).to_constructor(
            lambda: UserGrpcService(user_client)
        )

# En tu handler
class GetUserQueryHandler(QueryHandler):
    def __init__(self, user_service: UserGrpcService):
        self._user_service = user_service
    
    def handle(self, query: GetUserQuery) -> UserDTO:
        try:
            user_data = self._user_service.get_user(query.user_id)
            return UserDTO(**user_data)
        except UserNotFoundError:
            raise UserNotFoundError(f"User {query.user_id} not found")
        except GrpcServiceError as e:
            logger.error(f"gRPC service failed: {e}")
            raise ServiceUnavailableError("User service is currently unavailable")
```

El gRPC Client proporciona una interfaz robusta y type-safe para comunicación entre microservicios, con soporte completo para protobuf, manejo de errores, correlación de traces y tanto llamadas síncronas como asíncronas. 