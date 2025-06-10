
# Normas DDD del Proyecto

> Última actualización: 2025-06-11  
> Destinatarios: equipo backend y LLMs que generen código  

---

## 0. Configuración del proyecto

En el archivo pyproject.toml tienes la configuracion del proyecto. Debes fijarte en que:

- No hace falta declarar archivos __init__.py para importar

---

## 1. Regla de dependencias

```

Domain  ←  Application  ←  Infrastructure
↑             ↑                ↑
(depende de)  (depende de Domain)   (puede depender de Application y Domain)

```

- **Domain** nunca importa `Application` ni `Infrastructure`.  
- **Application** solo conoce `Domain` e interfaces.  
- **Infrastructure** implementa detalles técnicos y se inyecta por *dependency injection*.

---

## 2. Bounded Contexts y estructura de carpetas

```

app/
└── Contexts/
├── Shared/                       # Primitivas reutilizables (sin lógica de negocio)
└── <Context>/
    └── <Aggregate>/
        ├── Domain/
        ├── Application/
        │   ├── Create/
        │   ├── Search/
        │   ├── Update/
        │   └── Delete/
        └── Infrastructure/

````

- `Shared/` contiene solo primitivas.  
- La carpeta **Application** se divide **a primer nivel por tipo de caso de uso** (`Create`, `Search`, `Update`, `Delete`, …).  
- Cada subcarpeta de caso de uso alberga sus `Command`, `Query`, `Handler`, etc.

---

## 3. Comunicación entre contextos

1. Declara **interfaces** en `Shared/Application/<Nombre>Contract.py`.  
2. Implementa la interfaz en el contexto consumidor.  
3. Inyecta la interfaz, nunca la implementación concreta.

```python
# Shared/Application/UserContract.py
class UserContract(ABC):
    async def find(self, email: str) -> Optional[dict]: ...
````

---

## 4. Domain layer

* **Entidades** mantienen sus invariantes y reglas.
* **Value objects** son inmutables y encapsulados.
* **Aggregates** garantizan consistencia e incluyen `to_primitives` y `from_primitives`.
* Lógica transversal sin dueño → **domain services**.

### Naming de value objects

| Propósito          | Ejemplo correcto |
| ------------------ | ---------------- |
| Email de usuario   | `UserEmail`      |
| ID de usuario      | `UserId`         |
| Precio de producto | `ProductPrice`   |

---

## 5. Application layer

* Sigue **CQRS**: *commands* modifican, *queries* leen.
* *Handlers* solo orquestan; **nunca** contienen lógica de negocio.
* Usa un **event bus** para publicar eventos de dominio.
* La división de carpetas por caso de uso es obligatoria (ver sección 2).

---

## 6. Infrastructure layer

* Implementa repositorios, buses, adaptadores HTTP/GRPC, etc.
* Carece de reglas de negocio.
* Todas las dependencias se resuelven en el *bootstrap* mediante DI.

---

## 7. Anti-patrones que rompen la CI

| Problema                                      | Motivo                |
| --------------------------------------------- | --------------------- |
| `Domain` importando `PostgresUserRepository`  | Viola capas           |
| Entidad anémica + servicio con toda la lógica | *Anemic Domain Model* |
| Agregado con múltiples responsabilidades      | *God Aggregate*       |

---

## 8. Convenciones de naming

| Tipo         | Ejemplo                |
| ------------ | ---------------------- |
| Entity       | `User`, `Order`        |
| Value Object | `UserEmail`, `OrderId` |
| Command      | `CreateUserCommand`    |
| Event        | `UserCreatedEvent`     |

Usa siempre el *ubiquitous language* del dominio.

---

## 9. Checklist de pull request

* [ ] Dependencias cumplen `Domain ← Application ← Infrastructure`.
* [ ] Cada contexto y agregado tiene responsabilidad única.
* [ ] Carpetas de **Application** divididas por caso de uso (`Create`, `Search`, …).
* [ ] Application usa solo interfaces.
* [ ] Sin lógica de negocio en Infrastructure.
* [ ] Tests de capa para Domain y Application.

---

## 10. Estrategia de adopción

1. **Descubrimiento de dominio**

   * Workshops con negocio → glosario común y context maps.
2. **Definición de bounded contexts**

   * Identificar integridad y límites claros.
3. **Diseño incremental**

   * Modelar agregados mínimos viables; refactor continuo.
4. **Pipeline de calidad**

   * Lint + tests por capa + revisión de PR con checklist (sección 9).
5. **Capacitación continua**

   * Katas DDD internas; sesiones quincenales de revisión de modelo.

---

## 11. Instrucciones para LLM / script de automatización

1. **Escribe un documento* en la raíz del repositorio como `DDD_GUIDE.md` explicando los pasos que vas a realizar para completar la tarea.
2. **Commits**: usa el estándar *Conventional Commits* (tipo en minúsculas, mensaje en imperativo, ≤ 50 caracteres).

   * Ejemplos:

     * `docs: add DDD guide with strategy`
     * `feat(user): implement UserEmail value object`
     * `refactor(order): split aggregate into smaller roots`
3. **Commits atómicos**: un cambio funcional por commit; descripción adicional en cuerpo (80 caracteres por línea).
