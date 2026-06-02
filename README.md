# 🚀 Payflow Finance — MVP & CLI Integrado

¡Bienvenido a **Payflow Finance**! Este es el Producto Mínimo Viable (MVP) que integra todos los módulos del núcleo financiero de Payflow en una sola interfaz interactiva de terminal (CLI) y un paquete de Python profesional, limpio y modular.

El sistema funciona como un "Guardián" proactivo de la salud financiera del usuario, validando operaciones bancarias, automatizando suscripciones, controlando riesgos de inversión y aplicando descuentos especiales en transacciones.

---

## 📂 Arquitectura del Proyecto

El código está estructurado bajo estándares profesionales de empaquetado en Python:

```
kata_payflow_next/
├── payflow/                    # 🐍 Código de Producción (Paquete Principal)
│   ├── __init__.py             # Expone la API pública del sistema
│   ├── acceso.py               # Lógica de validación de acceso al sistema (RF-01)
│   ├── inversiones.py          # Lógica de cálculo de rendimientos y control de riesgos
│   ├── pagos.py                # Gestión de pagos de servicios (Renta, Luz, Internet)
│   ├── streaming.py            # Máquina de estados de suscripciones de streaming
│   ├── validador.py            # Validador bancario de perfiles de inversión
│   └── sistema.py              # Integrador de módulos y persistencia en disco
│
├── tests/                      # 🧪 Suite de Pruebas Unificada
│   ├── test_acceso.py          # Pruebas unitarias de acceso al sistema
│   ├── test_inversiones.py     # Pruebas unitarias de inversión
│   ├── test_pagos.py           # Pruebas unitarias de pagos
│   ├── test_streaming.py       # Pruebas de transiciones de estados de streaming
│   ├── test_validador.py       # Pruebas del calificador bancario
│   └── test_sistema.py         # Pruebas de integración del flujo de sistema
│
├── cli.py                      # 🖥️ Interfaz de Línea de Comandos Interactiva (Punto de entrada)
├── payflow_db.json             # 💾 Base de datos ligera (JSON)
├── pytest.ini                  # Configuración de pruebas
└── docs/                       # Diagramas de flujo y estados
```

---

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/SnakeGuitar/payflow-finance.git
   cd kata_payflow_next
   ```

2. **Crear e inicializar un entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   # En Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias necesarias para desarrollo/pruebas:**
   ```bash
   pip install pytest pytest-cov radon
   ```

---

## 🖥️ Interfaz de Consola (CLI)

Para iniciar la aplicación interactiva de Payflow, ejecuta:
```bash
python cli.py
```

El CLI es completamente interactivo y te permite:
* Crear y alternar entre usuarios (`Alice`, `Bob`, `Charlie`).
* Ver reportes financieros detallados con tablas de historial de transacciones e inversiones.
* Realizar pagos de servicios con **descuento del 100% en comisión fija ($0.00) para el concepto INTERNET**.
* Simular rendimientos de inversiones de bajo/alto riesgo y registrarlas en tiempo real.
* Controlar y avanzar los estados de suscripciones de streaming (`ACTIVO`, `MORA`, `SUSPENDIDO`, etc.) disparando eventos de cobros automáticos.

---

## 🧪 Comandos Útiles de Pruebas y Métricas

La suite de pruebas contiene **93 casos de prueba** que garantizan la integridad del sistema financiero.

### 1. Ejecutar la Suite de Pruebas
Ejecuta todos los archivos de prueba estructurados dentro de la carpeta `tests/`:
```bash
pytest
```

Para ver la salida detallada de cada prueba ejecutada:
```bash
pytest -v
```

### 2. Medición de Cobertura de Código (Coverage)
Para medir qué porcentaje de nuestro código de producción está cubierto por las pruebas automatizadas:

* **Reporte rápido en terminal:**
  ```bash
  pytest --cov=payflow tests/
  ```

* **Reporte detallado en terminal (muestra qué líneas exactas faltan de probar):**
  ```bash
  pytest --cov=payflow --cov-report=term-missing tests/
  ```

* **Generar reporte interactivo HTML (crea una carpeta `htmlcov/` con un visualizador web):**
  ```bash
  pytest --cov=payflow --cov-report=html tests/
  ```
  *(Puedes abrir `htmlcov/index.html` en cualquier navegador).*

### 3. Complejidad Ciclomática (Radon)
Radon mide la complejidad de las rutas de código (método McCabe). Un menor puntaje indica código más limpio y fácil de mantener (Rango A es el óptimo).

* **Revisar complejidad de la carpeta de producción:**
  ```bash
  radon cc payflow -s
  ```

* **Revisar el Índice de Mantenibilidad (Maintainability Index - MI):**
  ```bash
  radon mi payflow
  ```

* **Revisar métricas brutas (líneas de código físicas, lógicas, comentarios):**
  ```bash
  radon raw payflow
  ```

---

## ⚡ Tecnologías Utilizadas

* **Python 3.12.x** - Lenguaje base.
* **Pytest 9.x** - Framework de pruebas.
* **Pytest-Cov** - Analizador de cobertura.
* **Radon** - Analizador de complejidad y métricas de software.
* **JSON** - Persistencia de datos.
