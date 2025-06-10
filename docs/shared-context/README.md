# Contexto Shared - Documentación

El **Contexto Shared** implementa el patrón **Shared Kernel** de Domain-Driven Design (DDD), proporcionando primitivas de dominio, patrones de aplicación y utilidades de infraestructura reutilizables across todos los bounded contexts de Yurest.

## 🏗️ Arquitectura DDD

```
app/Contexts/Shared/
├── Domain/                    # 🏛️ Capa de Dominio
│   ├── ValueObject/           # Value Objects inmutables
│   ├── ExceptionHandling/     # Excepciones de dominio
│   ├── DomainEvent.py         # Eventos de dominio
│   ├── Clock/                 # Servicios de tiempo
│   └── Logging/               # Abstracciones de logging
├── Application/               # 🎯 Capa de Aplicación
│   ├── Bus/                   # Patrones CQRS
│   │   ├── Command/           # Command Bus
│   │   ├── Query/             # Query Bus
│   │   └── Event/             # Event Bus
│   └── Cache/                 # Servicios de caché
└── Infrastructure/            # 🔧 Capa de Infraestructura
    ├── Http/                  # Cliente HTTP
    │   ├── Client/            # HTTP Client
    │   ├── Context/           # Request Context
    │   ├── Controller.py      # Base Controller
    │   └── Middleware/        # Middlewares
    ├── Grpc/                  # Cliente gRPC
    │   └── Client/            # gRPC Client
    ├── Logging/               # Configuración de logs
    ├── Bootstrap/             # Application bootstrapping
    ├── Bus/                   # Implementaciones de buses
    ├── Cache/                 # Implementaciones de caché
    └── Module/                # Dependency injection
```

## 🎯 Propósito y Principios

### **Shared Kernel Pattern**
- Contiene **primitivas comunes** sin lógica de dominio específica
- **Reutilizable** across múltiples bounded contexts
- **Estable** y con cambios coordinados entre equipos

### **Separación por Capas DDD**
- **Domain**: Lógica de negocio pura, sin dependencias externas
- **Application**: Orquestación y patrones como CQRS
- **Infrastructure**: Implementaciones técnicas y frameworks

## 📚 Componentes Principales

### 🏛️ **Domain Layer**
- **[Value Objects](./domain/value-objects.md)**: Primitivas inmutables con validación
- **[Domain Events](./domain/domain-events.md)**: Eventos para comunicación entre bounded contexts
- **[Domain Services](./domain/domain-services.md)**: Servicios puros de dominio

### 🎯 **Application Layer**  
- **[CQRS Buses](./application/cqrs-buses.md)**: Command, Query y Event buses
- **[Cache Services](./application/cache-services.md)**: Abstracciones de caché
- **[Application Services](./application/application-services.md)**: Orquestación de use cases

### 🔧 **Infrastructure Layer**
- **[HTTP Client](./infrastructure/http-client.md)**: Cliente HTTP robusto
- **[gRPC Client](./infrastructure/grpc-client.md)**: Cliente gRPC con tipo seguro
- **[Request Context](./infrastructure/request-context.md)**: Manejo de contexto de request
- **[Logging](./infrastructure/logging.md)**: Configuración y logging estructurado
- **[Middleware](./infrastructure/middleware.md)**: Middlewares para FastAPI
- **[Bootstrap](./infrastructure/bootstrap.md)**: Inicialización de aplicación

## 🚀 Quick Start

### **Usar Value Objects**
```python
from app.Contexts.Shared.Domain.ValueObject.NumericValueObject import NumericValueObject

class Price(NumericValueObject[float]):
    def __init__(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        super().__init__(value)

price = Price(29.99)
print(price.value())  # 29.99
```

### **Usar CQRS Buses**
```python
from app.Contexts.Shared.Application.Bus.Command.CommandBus import CommandBus

# Inyectar el bus en tu handler
bus = container.get(CommandBus)
bus.dispatch(CreateUserCommand(name="John", email="john@example.com"))
```

### **Usar HTTP Client**
```python
from app.Contexts.Shared.Infrastructure.Http.Client.HttpClient import HttpClient

with HttpClient("https://api.example.com") as client:
    request = MyHttpRequest()
    response = client.send(request)
```

### **Usar Request Context**
```python
from app.Contexts.Shared.Infrastructure.Http.Context.RequestContext import RequestContext

trace_id = RequestContext.get_trace_id()
logger.info(f"Processing request")  # [trace_id] se incluye automáticamente
```

## 📖 Índice de Documentación

### 🏛️ **Domain Layer**
Primitivas de dominio puras, sin dependencias externas.

| Componente | Descripción | Documentación |
|------------|-------------|---------------|
| **Value Objects** | Primitivas inmutables con validación | [📖 Ver docs](./domain/value-objects.md) |
| **Domain Events** | Eventos de dominio para comunicación | [📖 Ver docs](./domain/domain-events.md) |
| **Domain Services** | Servicios puros de dominio | [📖 Ver docs](./domain/domain-services.md) |
| **Exception Handling** | Manejo de excepciones de dominio | [📖 Ver docs](./domain/exception-handling.md) |

### 🎯 **Application Layer**  
Patrones de aplicación y orquestación de use cases.

| Componente | Descripción | Documentación |
|------------|-------------|---------------|
| **CQRS Buses** | Command, Query y Event buses | [📖 Ver docs](./application/cqrs-buses.md) |
| **Cache Services** | Abstracciones de caché | [📖 Ver docs](./application/cache-services.md) |
| **Application Services** | Orquestación de casos de uso | [📖 Ver docs](./application/application-services.md) |

### 🔧 **Infrastructure Layer**
Implementaciones técnicas y utilidades de infraestructura.

| Componente | Descripción | Documentación |
|------------|-------------|---------------|
| **HTTP Client** | Cliente HTTP robusto y type-safe | [📖 Ver docs](./infrastructure/http-client.md) |
| **gRPC Client** | Cliente gRPC con protobuf | [📖 Ver docs](./infrastructure/grpc-client.md) |
| **Request Context** | Manejo de contexto de request | [📖 Ver docs](./infrastructure/request-context.md) |
| **Logging** | Configuración y logging estructurado | [📖 Ver docs](./infrastructure/logging.md) |
| **Middleware** | Middlewares para FastAPI | [📖 Ver docs](./infrastructure/middleware.md) |
| **Bootstrap** | Inicialización de aplicación | [📖 Ver docs](./infrastructure/bootstrap.md) |

### **📋 Patrones y Guías**
| Tipo | Descripción | Documentación |
|------|-------------|---------------|
| **Value Objects Pattern** | Inmutabilidad y validación | [📖 Ver docs](./patterns/value-objects-pattern.md) |
| **CQRS Pattern** | Separación de Command y Query | [📖 Ver docs](./patterns/cqrs-pattern.md) |
| **Request Context Pattern** | Correlación de traces | [📖 Ver docs](./patterns/request-context-pattern.md) |
| **Client Pattern** | Abstracción de clientes HTTP/gRPC | [📖 Ver docs](./patterns/client-pattern.md) |
| **Integración FastAPI** | Cómo integrar con FastAPI | [📖 Ver docs](./guides/fastapi-integration.md) |
| **Testing Strategies** | Estrategias de testing | [📖 Ver docs](./guides/testing-strategies.md) |
| **Performance** | Mejores prácticas de rendimiento | [📖 Ver docs](./guides/performance.md) |
| **Error Handling** | Manejo de errores robusto | [📖 Ver docs](./guides/error-handling.md) |

## 🛠️ Desarrollo

### **Añadir Nuevos Componentes**
1. Determina la **capa correcta** (Domain/Application/Infrastructure)
2. Sigue los **patrones existentes** y convenciones
3. Añade **tests unitarios** comprehensivos
4. Actualiza la **documentación**

### **Principios de Diseño**
- **Single Responsibility**: Cada clase tiene una responsabilidad clara
- **Dependency Inversion**: Depende de abstracciones, no implementaciones
- **Open/Closed**: Abierto para extensión, cerrado para modificación
- **Interface Segregation**: Interfaces pequeñas y cohesivas

## 📊 Estado de Componentes

### **Components Status**
| Componente | Estado | Versión | Cobertura Tests |
|------------|--------|---------|-----------------|
| Value Objects | 🚧 Nuevo | v1.0 | 0% |
| CQRS Buses | 🚧 Nuevo | v1.0 | 0% |
| HTTP Client | 🚧 Nuevo | v1.0 | 0% |
| gRPC Client | 🚧 Nuevo | v0.1 | 0% |
| Request Context | 🚧 Nuevo | v1.0 | 0% |
| Logging | 🚧 Nuevo | v1.0 | 0% |

## 📋 Roadmap

### **v0.2.0 - En desarrollo**
- [ ] Métricas y observabilidad
- [ ] Validación mejorada en Value Objects
- [ ] Soporte para streaming en gRPC
- [ ] Circuit breaker para HTTP client

### **v0.3.0 - Planificado**
- [ ] Message broker abstractions
- [ ] Database abstractions
- [ ] Configuration management
- [ ] Health checks framework

## 🤝 Contribución

Al ser un **Shared Kernel**, los cambios deben ser:
- **Coordinados** entre todos los equipos
- **Backward compatible** cuando sea posible
- **Bien testeados** y documentados
- **Revisados** por múltiples equipos

## 📞 Soporte

- **Documentación**: [docs/shared-context/](.)
- **Ejemplos**: [examples/](../examples/)
- **Issues**: Reportar en el repositorio principal
- **Discusiones**: Canal #shared-kernel en Slack 