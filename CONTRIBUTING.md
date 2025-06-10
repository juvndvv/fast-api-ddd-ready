# 🤝 Guía de Contribución

## ⚠️ Setup OBLIGATORIO para Desarrolladores

### 1. Primer Setup (UNA SOLA VEZ)
```bash
# Después de clonar el repositorio
git clone <repository-url>
cd yurest

# Instalar dependencias de desarrollo
uv sync --group dev

# ⚠️ OBLIGATORIO: Configurar pre-commit
uv run pre-commit install

# Verificar que todo funciona
uv run pre-commit run --all-files
./scripts/lint.sh
```

### 2. Verificación de Funcionamiento
Si todo está bien configurado, deberías ver:
```bash
✅ ruff.....................................................................Passed
✅ ruff-format..............................................................Passed  
✅ black....................................................................Passed
✅ Linting completado!
```

## 🚀 Flujo de Desarrollo

### Pre-commit Automático
**No necesitas hacer nada extra**, pre-commit se ejecuta automáticamente en cada commit:

```bash
git add .
git commit -m "feat: nueva funcionalidad"
# ⚡ Pre-commit se ejecuta automáticamente y:
#   - ✅ Corrige errores de linting (ruff)
#   - ✅ Formatea código (black + ruff-format)
#   - ❌ Bloquea commit si hay errores críticos
```

### Comandos de Desarrollo

**Linting manual (antes de commit):**
```bash
./scripts/lint.sh
```

**Tests:**
```bash
pytest tests/
```

**Si pre-commit falla:**
1. Revisa los errores mostrados
2. Corrige manualmente los problemas
3. Vuelve a hacer `git add .` y `git commit`

## 🛠️ Herramientas Configuradas

| Herramienta | Propósito | Ejecuta |
|-------------|-----------|---------|
| **Ruff** | Linting + Import sorting | Automático en pre-commit |
| **Black** | Formateo de código | Automático en pre-commit |
| **MyPy** | Verificación de tipos | Manual con `./scripts/lint.sh` |
| **Pre-commit** | Ejecutor automático | En cada `git commit` |

## ❌ Errores Comunes

### "Pre-commit no funciona"
```bash
# Solución: Reinstalar pre-commit
uv run pre-commit clean
uv run pre-commit install
```

### "Command not found: uv"
```bash
# Instalar uv primero
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "MyPy errors"
- Los errores de MyPy NO bloquean commits (pre-commit solo usa ruff/black)
- Ejecuta manualmente: `./scripts/lint.sh`
- Corrige errores de tipos antes de hacer push

## 🎯 Estándares de Código

### Obligatorio (automático)
- ✅ **Formato**: Black + Ruff-format
- ✅ **Linting**: Ruff (errores, imports, etc.)
- ✅ **Commits**: Pre-commit hooks activos

### Recomendado (manual)
- 🔧 **Tipos**: MyPy sin errores
- 📝 **Tests**: Cobertura > 80%
- 📚 **Docs**: Funciones documentadas 