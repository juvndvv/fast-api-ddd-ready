# CQRS Buses - Application Layer

Los **CQRS Buses** implementan el patrón **Command Query Responsibility Segregation**, proporcionando una arquitectura desacoplada para manejar commands, queries y events en la aplicación.

## 🎯 Propósito del CQRS

### **Separación de Responsabilidades**
- **Commands**: Modifican el estado del sistema
- **Queries**: Obtienen información sin modificar estado
- **Events**: Notifican cambios que han ocurrido

### **Beneficios**
- ✅ **Desacoplamiento**: Components se comunican through buses
- ✅ **Escalabilidad**: Commands y queries pueden optimizarse independientemente
- ✅ **Testabilidad**: Fácil testing con mocks
- ✅ **Flexibilidad**: Fácil añadir middleware y interceptors

## 🏗️ Arquitectura

```
Application/Bus/
├── Command/
│   ├── Command.py              # Interfaz base para commands
│   ├── CommandHandler.py       # Interfaz para handlers
│   └── CommandBus.py          # Bus abstracto
├── Query/
│   ├── Query.py               # Interfaz base para queries
│   ├── QueryHandler.py        # Interfaz para handlers
│   └── QueryBus.py           # Bus abstracto
└── Event/
    ├── Event.py               # Interfaz base para events
    ├── EventListener.py       # Interfaz para listeners
    └── EventBus.py           # Bus abstracto
```

## 📋 Command Bus

### **Concepto**
Los **Commands** representan intenciones de cambiar el estado del sistema. Son imperativos y no devuelven valores.

### **Estructura**
```python
from app.Contexts.Shared.Application.Bus.Command.Command import Command
from app.Contexts.Shared.Application.Bus.Command.CommandHandler import CommandHandler
from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus

# 1. Definir Command
class CreateUserCommand(Command):
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

# 2. Definir Handler
class CreateUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def handle(self, command: CreateUserCommand) -> None:
        # Validaciones de negocio
        if command.age < 18:
            raise ValueError("User must be at least 18 years old")
        
        # Crear entity
        user = User.create(
            name=command.name,
            email=command.email,
            age=command.age
        )
        
        # Persistir
        self._user_repository.save(user)

# 3. Usar el Bus
bus = container.get(CommandBus)
command = CreateUserCommand("John Doe", "john@example.com", 25)
bus.dispatch(command)
```

### **Ejemplos de Commands**
```python
# Command para actualizar
class UpdateUserCommand(Command):
    def __init__(self, user_id: str, name: str = None, email: str = None):
        self.user_id = user_id
        self.name = name
        self.email = email

# Command para eliminar
class DeleteUserCommand(Command):
    def __init__(self, user_id: str):
        self.user_id = user_id

# Command para operaciones complejas
class ProcessPaymentCommand(Command):
    def __init__(self, order_id: str, amount: float, payment_method: str):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
```

## 🔍 Query Bus

### **Concepto**
Las **Queries** obtienen información del sistema sin modificar el estado. Son idempotentes y devuelven datos.

### **Estructura**
```python
from app.Contexts.Shared.Application.Bus.Query.Query import Query
from app.Contexts.Shared.Application.Bus.Query.QueryHandler import QueryHandler
from app.Contexts.Shared.Application.Bus.Query.QueryBus import QueryBus

# 1. Definir Query
class GetUserQuery(Query):
    def __init__(self, user_id: str):
        self.user_id = user_id

# 2. Definir Handler
class GetUserQueryHandler(QueryHandler):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def handle(self, query: GetUserQuery) -> UserDTO:
        user = self._user_repository.find_by_id(query.user_id)
        
        if not user:
            raise UserNotFoundError(f"User {query.user_id} not found")
        
        return UserDTO(
            id=user.id.value(),
            name=user.name.value(),
            email=user.email.value(),
            created_at=user.created_at.value()
        )

# 3. Usar el Bus
bus = container.get(QueryBus)
query = GetUserQuery("123")
user_dto = bus.ask(query)
```

### **Tipos de Queries**
```python
# Query simple
class GetUserByEmailQuery(Query):
    def __init__(self, email: str):
        self.email = email

# Query con filtros
class SearchUsersQuery(Query):
    def __init__(self, name: str = None, age_min: int = None, limit: int = 10):
        self.name = name
        self.age_min = age_min
        self.limit = limit

# Query con paginación
class GetUsersPagedQuery(Query):
    def __init__(self, page: int = 1, size: int = 20, sort_by: str = "created_at"):
        self.page = page
        self.size = size
        self.sort_by = sort_by

# Query agregada
class GetUserStatisticsQuery(Query):
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
```

## 📡 Event Bus

### **Concepto**
Los **Events** notifican que algo ha ocurrido en el sistema. Permiten comunicación asíncrona entre bounded contexts.

### **Estructura**
```python
from app.Contexts.Shared.Application.Bus.Event.Event import Event
from app.Contexts.Shared.Application.Bus.Event.EventListener import EventListener
from app.Contexts.Shared.Application.Bus.Event.EventBus import EventBus

# 1. Definir Event
class UserCreatedEvent(Event):
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.occurred_at = datetime.now(UTC)

# 2. Definir Listeners
class SendWelcomeEmailListener(EventListener):
    def __init__(self, email_service: EmailService):
        self._email_service = email_service
    
    def listen(self, event: UserCreatedEvent) -> None:
        self._email_service.send_welcome_email(
            email=event.email,
            name=event.name
        )

class UpdateAnalyticsListener(EventListener):
    def __init__(self, analytics_service: AnalyticsService):
        self._analytics_service = analytics_service
    
    def listen(self, event: UserCreatedEvent) -> None:
        self._analytics_service.track_user_registration(
            user_id=event.user_id
        )

# 3. Usar el Bus
bus = container.get(EventBus)
event = UserCreatedEvent("123", "John Doe", "john@example.com")
bus.publish(event)  # Todos los listeners se ejecutan
```

## 🔧 Configuración con Dependency Injection

### **Registro de Handlers**
```python
from app.Contexts.Shared.Infrastructure.Module.ApplicationModule import ApplicationModule

class UserModule(ApplicationModule):
    def map_commands(self) -> list[tuple[type[Command], CommandHandler]]:
        return [
            (CreateUserCommand, CreateUserCommandHandler),
            (UpdateUserCommand, UpdateUserCommandHandler),
            (DeleteUserCommand, DeleteUserCommandHandler),
        ]
    
    def map_queries(self) -> list[tuple[type[Query], QueryHandler]]:
        return [
            (GetUserQuery, GetUserQueryHandler),
            (SearchUsersQuery, SearchUsersQueryHandler),
            (GetUsersPagedQuery, GetUsersPagedQueryHandler),
        ]
    
    def map_events(self) -> list[tuple[type[Event], list[EventListener]]]:
        return [
            (UserCreatedEvent, [
                SendWelcomeEmailListener,
                UpdateAnalyticsListener,
                CreateUserProfileListener,
            ]),
            (UserUpdatedEvent, [
                NotifyUserChangesListener,
            ]),
        ]
```

## 💡 Patrones Avanzados

### **1. Command con Result**
```python
class CreateUserCommand(Command):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class CreateUserCommandHandler(CommandHandler):
    def handle(self, command: CreateUserCommand) -> str:  # Devuelve user_id
        user = User.create(command.name, command.email)
        self._user_repository.save(user)
        return user.id.value()
```

### **2. Query con Cache**
```python
class GetUserQueryHandler(QueryHandler):
    def __init__(self, user_repository: UserRepository, cache: CacheService):
        self._user_repository = user_repository
        self._cache = cache
    
    def handle(self, query: GetUserQuery) -> UserDTO:
        # Intentar desde cache
        cached = self._cache.get(f"user:{query.user_id}")
        if cached:
            return UserDTO.from_json(cached)
        
        # Obtener desde repository
        user = self._user_repository.find_by_id(query.user_id)
        user_dto = UserDTO.from_entity(user)
        
        # Guardar en cache
        self._cache.set(f"user:{query.user_id}", user_dto.to_json())
        
        return user_dto
```

### **3. Event Sourcing**
```python
class DomainEventHandler(EventListener):
    def __init__(self, event_store: EventStore):
        self._event_store = event_store
    
    def listen(self, event: Event) -> None:
        # Guardar evento para event sourcing
        self._event_store.append(event)
```

### **4. Middleware para Buses**
```python
class LoggingCommandMiddleware:
    def __init__(self, next_handler: CommandHandler):
        self._next = next_handler
        self._logger = logging.getLogger(__name__)
    
    def handle(self, command: Command) -> None:
        self._logger.info(f"Executing command: {command.__class__.__name__}")
        
        try:
            result = self._next.handle(command)
            self._logger.info(f"Command executed successfully")
            return result
        except Exception as e:
            self._logger.error(f"Command failed: {str(e)}")
            raise
```

## 🧪 Testing

### **Testing Commands**
```python
import pytest
from unittest.mock import Mock

class TestCreateUserCommandHandler:
    def test_handle_creates_user_successfully(self):
        # Arrange
        user_repository = Mock()
        handler = CreateUserCommandHandler(user_repository)
        command = CreateUserCommand("John Doe", "john@example.com", 25)
        
        # Act
        handler.handle(command)
        
        # Assert
        user_repository.save.assert_called_once()
        saved_user = user_repository.save.call_args[0][0]
        assert saved_user.name.value() == "John Doe"
        assert saved_user.email.value() == "john@example.com"
    
    def test_handle_raises_error_for_underage_user(self):
        # Arrange
        user_repository = Mock()
        handler = CreateUserCommandHandler(user_repository)
        command = CreateUserCommand("Jane Doe", "jane@example.com", 16)
        
        # Act & Assert
        with pytest.raises(ValueError, match="User must be at least 18"):
            handler.handle(command)
        
        user_repository.save.assert_not_called()
```

### **Testing Queries**
```python
class TestGetUserQueryHandler:
    def test_handle_returns_user_dto(self):
        # Arrange
        user_repository = Mock()
        user = User.create("John Doe", "john@example.com", 25)
        user_repository.find_by_id.return_value = user
        
        handler = GetUserQueryHandler(user_repository)
        query = GetUserQuery("123")
        
        # Act
        result = handler.handle(query)
        
        # Assert
        assert isinstance(result, UserDTO)
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
```

### **Testing Events**
```python
class TestUserCreatedEventListeners:
    def test_send_welcome_email_listener(self):
        # Arrange
        email_service = Mock()
        listener = SendWelcomeEmailListener(email_service)
        event = UserCreatedEvent("123", "John Doe", "john@example.com")
        
        # Act
        listener.listen(event)
        
        # Assert
        email_service.send_welcome_email.assert_called_once_with(
            email="john@example.com",
            name="John Doe"
        )
```

## 🔗 Integración con Controllers

### **En FastAPI Controllers**
```python
from app.Contexts.Shared.Infrastructure.Http.Controller import Controller

class UserController(Controller):
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus
    
    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.add_api_route("/users", self.create_user, methods=["POST"])
        router.add_api_route("/users/{user_id}", self.get_user, methods=["GET"])
        return router
    
    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        command = CreateUserCommand(
            name=request.name,
            email=request.email,
            age=request.age
        )
        
        user_id = self._command_bus.dispatch(command)
        
        return CreateUserResponse(
            user_id=user_id,
            message="User created successfully"
        )
    
    async def get_user(self, user_id: str) -> UserResponse:
        query = GetUserQuery(user_id)
        user_dto = self._query_bus.ask(query)
        
        return UserResponse(
            id=user_dto.id,
            name=user_dto.name,
            email=user_dto.email,
            created_at=user_dto.created_at
        )
```

Los CQRS Buses proporcionan una arquitectura limpia y escalable para manejar la lógica de aplicación, manteniendo la separación de responsabilidades y facilitando el testing y mantenimiento del código. 