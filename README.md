# Yurest

Proyecto principal que implementa Domain-Driven Design (DDD) con arquitectura de microservicios.

## 📁 Estructura del Proyecto

```
app/
├── Contexts/
│   ├── Shared/           # 🔗 Contexto Shared (Shared Kernel)
│   ├── User/             # Contexto de Usuario  
│   ├── Order/            # Contexto de Pedidos
│   └── ...               # Otros bounded contexts
├── docs/                 # Documentación
└── tests/               # Tests
```

## 🏛️ Contexto Shared (Shared Kernel)

El **Contexto Shared** implementa el patrón **Shared Kernel** de DDD, proporcionando primitivas de dominio, patrones de aplicación y utilidades de infraestructura reutilizables.

### **Componentes Principales**
- 🏛️ **Value Objects**: Primitivas inmutables con validación
- 🎯 **CQRS Buses**: Command, Query y Event buses
- 🌐 **HTTP/gRPC Clients**: Clientes type-safe para comunicación
- 🔍 **Request Context**: Correlación automática de traces
- 📝 **Logging**: Sistema de logging estructurado

➡️ **[📖 Ver documentación completa del Contexto Shared](./docs/shared-context/README.md)**

## 📖 Bounded Contexts

### **🏛️ Contextos Disponibles**
| Contexto | Estado | Descripción |
|----------|--------|-------------|
| **[Shared](./docs/shared-context/README.md)** | ✅ Activo | Shared Kernel con primitivas comunes |
| **User** | 🚧 En desarrollo | Gestión de usuarios |
| **Order** | 📋 Planificado | Gestión de pedidos |
| **Payment** | 📋 Planificado | Procesamiento de pagos |

## 🚀 Quick Start

### **Setup del Proyecto**
```bash
# Clonar el repositorio
git clone <repository-url>
cd yurest

# Con uv (recomendado)
uv sync --group dev
uv run pre-commit install

# O con pip tradicional
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
pre-commit install
```

### **Ejemplo de Uso**
```python
# Usar Value Objects del Shared Context
from app.Contexts.Shared.Domain.ValueObject.NumericValueObject import NumericValueObject

class Price(NumericValueObject[float]):
    def __init__(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        super().__init__(value)

price = Price(29.99)
print(price.value())  # 29.99
```

## 🛠️ Desarrollo

### **Configuración de Desarrollo** ⚠️
**IMPORTANTE**: Después de clonar, ejecutar:
```bash
# Instalar dependencias de desarrollo
uv sync --group dev

# Configurar pre-commit (OBLIGATORIO para commits)
uv run pre-commit install

# Verificar configuración
uv run pre-commit run --all-files
```

### **Linting y Formateo**
```bash
# Ejecutar linting completo (automático)
./scripts/lint.sh

# Comandos individuales
uv run ruff check app/ --fix    # Linting + corrección
uv run black app/               # Formateo
uv run mypy --config-file mypy.ini  # Verificación de tipos
```

### **Ejecutar Tests**
```bash
# Tests unitarios
pytest tests/

# Coverage de Shared Context específicamente
pytest --cov=app.Contexts.Shared tests/Contexts/Shared/
```

### **Estructura de Comandos**
```bash
# Ver estructura del proyecto
tree app/Contexts/

# Ejecutar ejemplos
python examples/shared_context_examples.py
```

## 📚 Documentación

### **📖 Documentación Disponible**
- **[Contexto Shared](./docs/shared-context/README.md)** - Shared Kernel completo
- **Contextos de Dominio** - *(Próximamente)*

### **🔗 Enlaces Útiles**
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Shared Kernel Pattern](https://martinfowler.com/bliki/BoundedContext.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)

## 📞 Soporte

- **📚 Documentación**: Ver sección anterior
- **🐛 Issues**: Reportar problemas en el repositorio
- **💬 Discusiones**: Canal #yurest-dev en Slack

---

**📈 Última actualización**: Enero 2024  
**👥 Mantenedores**: Equipo Yurest  
**📝 Versión**: v1.0
