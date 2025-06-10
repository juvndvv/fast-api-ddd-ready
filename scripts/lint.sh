#!/bin/bash

echo "🔍 Ejecutando linting completo..."

echo "📋 1. Ruff (linting y import sorting)..."
ruff check app/ --fix

echo "🎨 2. Black (formateo automático)..."
black app/

echo "🔧 3. MyPy (verificación de tipos)..."
mypy --config-file mypy.ini

echo "✅ Linting completado!" 