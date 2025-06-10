# Value Objects - Domain Layer

Los **Value Objects** son primitivas inmutables que encapsulan valores simples con validación y comportamiento específico del dominio. Son uno de los building blocks fundamentales en DDD.

## 🎯 Propósito

### **Características de Value Objects**
- **Inmutables**: No pueden cambiar después de su creación
- **Validación**: Garantizan que siempre contienen datos válidos
- **Comportamiento**: Encapsulan lógica relacionada con el valor
- **Comparación por valor**: Dos value objects son iguales si sus valores son iguales

### **Beneficios**
- ✅ **Type Safety**: Evita errores de primitivas obsesión
- ✅ **Validación centralizada**: Una sola lugar para reglas de validación
- ✅ **Expresividad**: El código es más legible y expresivo
- ✅ **Reutilización**: Se pueden usar en múltiples bounded contexts

## 🏗️ Arquitectura

```
Domain/ValueObject/
├── ValueObject.py              # Clase base abstracta
├── NumericValueObject.py       # Para valores numéricos (int, float)
├── IntegerValueObject.py       # Especialización para enteros
├── StringValueObject.py        # Para valores de texto
└── DateTimeValueObject.py      # Para fechas y timestamps
```

## 📚 Value Objects Disponibles

### **1. ValueObject (Base)**
Clase base abstracta que define el contrato para todos los value objects.

```python
from app.Contexts.Shared.Domain.ValueObject.ValueObject import ValueObject

class CustomValue(ValueObject[str]):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Value cannot be empty")
        super().__init__(value)
    
    def value(self) -> str:
        return self._value
```

### **2. NumericValueObject**
Para valores numéricos con operaciones matemáticas.

```python
from app.Contexts.Shared.Domain.ValueObject.NumericValueObject import NumericValueObject

class Price(NumericValueObject[float]):
    def __init__(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        super().__init__(value)
    
    def add_tax(self, tax_rate: float) -> float:
        return self.value() * (1 + tax_rate)

# Uso
price = Price(100.0)
price_with_tax = price.add_tax(0.21)  # 121.0

# Operaciones matemáticas
total = price + Price(50.0)  # 150.0
```

### **3. IntegerValueObject**
Especialización para números enteros.

```python
from app.Contexts.Shared.Domain.ValueObject.IntegerValueObject import IntegerValueObject

class Quantity(IntegerValueObject):
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        super().__init__(value)
    
    def is_bulk_order(self) -> bool:
        return self.value() >= 100

# Uso
qty = Quantity(150)
print(qty.is_bulk_order())  # True
```

### **4. StringValueObject**
Para valores de texto con validaciones específicas.

```python
from app.Contexts.Shared.Domain.ValueObject.StringValueObject import StringValueObject

class Email(StringValueObject):
    def __init__(self, value: str):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email format")
        super().__init__(value.lower())
    
    def _is_valid_email(self, email: str) -> bool:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def domain(self) -> str:
        return self.value().split('@')[1]

# Uso
email = Email("USER@EXAMPLE.COM")
print(email.value())    # user@example.com
print(email.domain())   # example.com
```

### **5. DateTimeValueObject**
Para fechas y timestamps.

```python
from app.Contexts.Shared.Domain.ValueObject.DateTimeValueObject import DateTimeValueObject
from datetime import datetime, UTC

class CreatedAt(DateTimeValueObject):
    def __init__(self, value: datetime = None):
        if value is None:
            value = datetime.now(UTC)
        super().__init__(value)
    
    def is_recent(self, hours: int = 24) -> bool:
        now = datetime.now(UTC)
        return (now - self.value()).total_seconds() < (hours * 3600)

# Uso
created = CreatedAt()
print(created.is_recent())  # True
```

## 💡 Patrones de Uso

### **1. Value Objects Compuestos**
```python
class Address(ValueObject[dict]):
    def __init__(self, street: str, city: str, postal_code: str):
        if not all([street, city, postal_code]):
            raise ValueError("All address fields are required")
        
        self._street = street
        self._city = city
        self._postal_code = postal_code
    
    def value(self) -> dict:
        return {
            "street": self._street,
            "city": self._city,
            "postal_code": self._postal_code
        }
    
    def full_address(self) -> str:
        return f"{self._street}, {self._city} {self._postal_code}"
```

### **2. Value Objects con Validaciones Complejas**
```python
class PhoneNumber(StringValueObject):
    def __init__(self, value: str):
        cleaned = self._clean_phone(value)
        if not self._is_valid_phone(cleaned):
            raise ValueError("Invalid phone number")
        super().__init__(cleaned)
    
    def _clean_phone(self, phone: str) -> str:
        # Remover espacios, guiones, paréntesis
        return ''.join(filter(str.isdigit, phone))
    
    def _is_valid_phone(self, phone: str) -> bool:
        return len(phone) >= 10 and phone.isdigit()
    
    def formatted(self) -> str:
        phone = self.value()
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
```

### **3. Value Objects para Identificadores**
```python
class UserId(StringValueObject):
    def __init__(self, value: str = None):
        if value is None:
            value = str(uuid.uuid4())
        
        if not self._is_valid_uuid(value):
            raise ValueError("Invalid UUID format")
        
        super().__init__(value)
    
    def _is_valid_uuid(self, value: str) -> bool:
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False
```

## 🧪 Testing

### **Test de Value Objects**
```python
import pytest
from your_domain import Price, Email

class TestPrice:
    def test_valid_price_creation(self):
        price = Price(100.0)
        assert price.value() == 100.0
    
    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Price(-10.0)
    
    def test_price_equality(self):
        price1 = Price(100.0)
        price2 = Price(100.0)
        assert price1 == price2
    
    def test_price_mathematical_operations(self):
        price1 = Price(100.0)
        price2 = Price(50.0)
        assert price1 + price2 == 150.0

class TestEmail:
    def test_valid_email_creation(self):
        email = Email("test@example.com")
        assert email.value() == "test@example.com"
    
    def test_email_normalization(self):
        email = Email("TEST@EXAMPLE.COM")
        assert email.value() == "test@example.com"
    
    def test_invalid_email_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Email("invalid-email")
    
    def test_email_domain_extraction(self):
        email = Email("user@example.com")
        assert email.domain() == "example.com"
```

## 🔧 Mejores Prácticas

### **✅ Buenas Prácticas**
```python
# ✅ Validación en constructor
class Age(IntegerValueObject):
    def __init__(self, value: int):
        if not 0 <= value <= 150:
            raise ValueError("Age must be between 0 and 150")
        super().__init__(value)

# ✅ Métodos de comportamiento específico del dominio
class Temperature(NumericValueObject[float]):
    def to_fahrenheit(self) -> float:
        return (self.value() * 9/5) + 32
    
    def is_freezing(self) -> bool:
        return self.value() <= 0

# ✅ Factory methods para casos comunes
class Status(StringValueObject):
    @classmethod
    def pending(cls) -> 'Status':
        return cls("PENDING")
    
    @classmethod
    def completed(cls) -> 'Status':
        return cls("COMPLETED")
```

### **❌ Anti-patrones**
```python
# ❌ No añadir lógica que no pertenece al value object
class Price(NumericValueObject[float]):
    def save_to_database(self):  # ❌ Responsabilidad de infraestructura
        pass
    
    def send_notification(self):  # ❌ Responsabilidad de aplicación
        pass

# ❌ No hacer value objects mutables
class MutablePrice(NumericValueObject[float]):
    def set_value(self, new_value: float):  # ❌ Rompe inmutabilidad
        self._value = new_value

# ❌ No usar value objects para entidades
class User(StringValueObject):  # ❌ User debería ser una Entity
    pass
```

## 🔗 Integración con Bounded Contexts

### **Reutilización entre Contextos**
```python
# En contexto de User
class UserEmail(Email):
    pass

# En contexto de Order
class OrderId(StringValueObject):
    def __init__(self, value: str = None):
        if value is None:
            value = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().__init__(value)

# En contexto de Payment
class Amount(Price):
    def format_currency(self, currency: str = "USD") -> str:
        return f"{self.value():.2f} {currency}"
```

Los Value Objects del contexto Shared proporcionan la base sólida para construir value objects específicos de dominio en cada bounded context, manteniendo la consistencia y reutilización de validaciones y comportamientos comunes. 