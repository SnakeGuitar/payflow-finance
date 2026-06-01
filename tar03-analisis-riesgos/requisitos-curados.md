
## 1. Módulo de Acceso y Seguridad (PR01)

### RF-01: Validación de Acceso al Sistema

* **Descripción:** El sistema debe restringir el acceso a la plataforma basándose en la mayoría de edad del usuario y la presentación de un documento de identidad válido.
* **Reglas de Negocio:**
  * **Condición de Éxito:** Si (Edad $\ge 18$) **Y** (ID Presentado = True), el sistema devuelve `ACCESO_CONCEDIDO`.
  * **Condición de Rechazo:** Si cualquiera de las dos condiciones anteriores es falsa, el sistema devuelve `ACCESO_DENEGADO`.

---

## 2. Módulo de Gestión de Suscripciones (PR02)

### RF-02: Procesamiento de Pagos Automáticos de Suscripciones

* **Descripción:** El sistema debe ejecutar los cobros recurrentes de las suscripciones digitales activas de los usuarios.
* **Reglas de Negocio:**
  * Un pago se considera **exitoso** si cumple simultáneamente:
    1. **Saldo:** Saldo disponible $\ge$ Costo de la suscripción.
    2. **Estado de Cuenta:** La cuenta NO está en estado `BLOQUEADA`.
    3. **Vigencia:** La tarjeta de crédito asociada NO está vencida.
  * **Excepción VIP:** Si el usuario posee estatus `VIP`, el pago se procesará con éxito aun si la tarjeta está vencida (manteniendo las restricciones de saldo y cuenta activa), pero el sistema **debe disparar obligatoriamente una notificación de aviso** al usuario.

---

## 3. Módulo de Priorización Presupuestal (PR03)

### RF-03: Validación y Cambio de Estado Presupuestal Mensual

* **Descripción:** El primer día de cada mes, el sistema debe evaluar el Presupuesto Mensual Total (PMT) frente a las proyecciones de gasto para determinar el estado operativo del periodo.
* **Reglas de Negocio:**
  * El sistema transitará de `Configuración de Fondos` a:
    * `Ejercicio`: Si el PMT cubre la totalidad de las prioridades de gasto.
    * `Ejercicio en Déficit`: Si el PMT es insuficiente en algún punto de la validación en cascada. Se deberán emitir alertas de déficit diferenciadas según el nivel donde se rompa el presupuesto.
  * **Algoritmo de Priorización (Cascada de Fondos):**
    1. **Prioridad 1 (Meta de Ahorro):** Se reserva el importe íntegro de la meta antes de distribuir a cualquier gasto.
    2. **Prioridad 2 (Servicios del Hogar):** Gastos variables calculados con base en el promedio anual histórico por rubro.
    3. **Prioridad 3 (Suscripciones Digitales):** Costos fijos mensuales.
    4. **Prioridad 4 (Ocio):** Gastos variables contrastados contra el promedio mensual de los últimos 6 meses.

---

## 4. Módulo de Transferencias Bancarias (PR04)

### RF-04: Ejecución de Transferencias e Interconexión de Cuentas

* **Descripción:** El sistema debe procesar solicitudes de envío de dinero recibiendo como parámetros: monto, hora de la transferencia (0-23 hrs) y tipo de cuenta destino (`Misma`, `Débito`, `Crédito`).
* **Reglas de Negocio / Matriz de Transición:**
  * **Regla de Mismo Banco:** Si el destino es `Misma`, la transferencia se aprueba inmediatamente (sujeta solo a saldo disponible), ignorando restricciones de horario o montos máximos.
  * **Regla de Horario (`Crédito`):** Las transferencias hacia cuentas de tipo `Crédito` solo se permiten en el rango de `09:00` a `18:00` hrs.
  * **Regla de Montos (`Débito`):** Si el destino es `Débito`, el monto máximo permitido sin validación extra es de `$5,000`. Montos mayores ($> \$5,000$) requieren estrictamente que el parámetro `token_activo` sea igual a `True`.
  * **Control de Estados:** Toda transferencia inicia en `PENDIENTE` y debe transitar únicamente a `APROBADA` o `RECHAZADA_POR_POLÍTICA`.

---

## 5. Módulo de Inversiones (PR05)

### RF-05: Lógica Matemática de Rendimientos (Capa Inferior)

* **Descripción:** El sistema calculará el interés compuesto para proyectar el monto final de una inversión.
* **Reglas de Negocio:**
  * **Fórmula:** El monto final $A$ se calcula mediante:
    $$
    = P(1 + r)^n
    $$

    Donde $P = \text{Capital a invertir}$, $r = \text{Tasa de interés mensual}$, y $n = \text{Tiempo en meses}$.
  * **Asignación de Tasa ($r$):**
    * Perfil Bajo Riesgo: 5% anual ($\approx 0.05 / 12$ mensual o según la convención de la práctica).
    * Perfil Alto Riesgo: 12% anual ($\approx 0.12 / 12$ mensual o según la convención de la práctica).
  * **Validación de Entrada:** Se rechazarán de inmediato plazos ($n$) menores a 12 meses (1 año) o montos de capital ($P$) negativos.

### RF-06: Gestión de Estados de Inversión (Capa Superior)

* **Descripción:** Controlar el impacto de la inversión sobre la salud financiera de la cuenta del usuario.
* **Reglas de Negocio:**
  * El sistema inicia en estado `DISPONIBLE`.
  * **Transición por Monto:**
    * Si el capital invertido es $> 50\%$ del saldo actual $\rightarrow$ Transita a `INVERSION_RIESGOSA`.
    * Si el capital invertido es $\le 50\%$ del saldo actual $\rightarrow$ Transita a `INVERSION_ESTABLE`.
  * **Restricción de Antigüedad:** Si el usuario tiene el estado `CUENTA_NUEVA` (antigüedad $< 3$ meses), tiene **estrictamente prohibido** seleccionar el perfil de "Alto Riesgo".

### RF-07: Integración y Generación de Folios (Capa Media)

* **Descripción:** Orquestar la validación simultánea de las capas inferior y superior para autorizar la inversión y emitir el comprobante.
* **Reglas de Negocio:**
  * **Criterio de Autorización:** Para que una inversión sea aprobada, debe cumplirse al mismo tiempo que el saldo sea suficiente para cubrir el capital $P$ **Y** que el perfil de riesgo sea compatible con la antigüedad de la cuenta.
  * **Estructura del Folio de Aprobación:** Solo si la inversión es `AUTORIZADA`, se generará una cadena con el formato: `<PERFIL>-<ESTADO>-<MONTO_FINAL_REDONDEADO>`.
    * *Codificación Perfil:* `B` (Bajo riesgo), `A` (Alto riesgo).
    * *Codificación Estado:* `E` (Inversión estable), `R` (Inversión riesgosa).
    * *Ejemplo:* Perfil bajo riesgo, estable, con monto final de \$1,250.75 $\rightarrow$ `B-E-1251`.
  * **Condición de Disparo Negativa:** Si la inversión es **RECHAZADA** (por saldo insuficiente o por restricción de cuenta nueva), el folio devuelto debe ser obligatoriamente `None` o un string vacío (`""`).
