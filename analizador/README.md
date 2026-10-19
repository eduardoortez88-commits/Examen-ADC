# Analizador de representación de datos

Aplicación web hecha con Python y Django que relaciona los sistemas numéricos con la codificación de caracteres.

## Qué hace

**Formulario 1: número**
- Se escribe un número y se elige su base de origen: 2, 8, 10 o 16.
- Valida que los dígitos pertenezcan a la base y que el valor esté entre 0 y 65 535.
- Muestra el resultado en decimal, binario (completado a 8, 16, 24... bits), octal y hexadecimal.
- Muestra los bits significativos y los bytes necesarios.

**Formulario 2: texto**
- Acepta hasta 20 caracteres.
- Para cada carácter muestra: carácter, código decimal, punto de código U+, hexadecimal y bytes UTF-8.

**Mensajes de error** para entrada vacía, dígitos inválidos, valores negativos, valores fuera de rango y texto de más de 20 caracteres.

## Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate
pip install "Django>=5.1,<5.3" gunicorn
python manage.py runserver
```

Abrir http://localhost:8000

## Pruebas automatizadas

```bash
python manage.py test -v 2
```

Son 15 pruebas: conversiones válidas, errores de base y de rango, y un caso UTF-8 con la letra ñ (decimal 241, U+00F1, bytes C3 B1).