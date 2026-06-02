from payflow.transferencia import Transferencia

# 1. Regla de Mismo Banco (Misma)
def test_transferencia_misma_cuenta_exitosa():
    t = Transferencia(10000.0)
    assert t.estado == "PENDIENTE"
    
    # Mismo banco no restringe por horario (ej: 3:00 AM) ni requiere token para montos > 5000
    exito, msg = t.procesar_transferencia(6000.0, 3, "Misma", token_activo=False)
    assert exito is True
    assert t.estado == "APROBADA"
    assert t.saldo_disponible == 4000.0

def test_transferencia_misma_cuenta_saldo_insuficiente():
    t = Transferencia(500.0)
    exito, msg = t.procesar_transferencia(600.0, 12, "Misma")
    assert exito is False
    assert t.estado == "RECHAZADA_POR_POLÍTICA"
    assert t.saldo_disponible == 500.0


# 2. Regla de Horario (Crédito)
def test_transferencia_credito_horario_permitido():
    # Rango 9:00 a 18:00 es permitido
    t1 = Transferencia(2000.0)
    exito1, _ = t1.procesar_transferencia(500.0, 9, "Crédito")
    assert exito1 is True
    assert t1.estado == "APROBADA"

    t2 = Transferencia(2000.0)
    exito2, _ = t2.procesar_transferencia(500.0, 18, "Crédito")
    assert exito2 is True
    assert t2.estado == "APROBADA"

    t3 = Transferencia(2000.0)
    exito3, _ = t3.procesar_transferencia(500.0, 14, "Crédito")
    assert exito3 is True
    assert t3.estado == "APROBADA"

def test_transferencia_credito_horario_no_permitido():
    # Rango fuera de 9:00 a 18:00 es rechazado
    t1 = Transferencia(2000.0)
    exito1, msg1 = t1.procesar_transferencia(500.0, 8, "Crédito")
    assert exito1 is False
    assert t1.estado == "RECHAZADA_POR_POLÍTICA"

    t2 = Transferencia(2000.0)
    exito2, msg2 = t2.procesar_transferencia(500.0, 19, "Crédito")
    assert exito2 is False
    assert t2.estado == "RECHAZADA_POR_POLÍTICA"


# 3. Regla de Montos (Débito)
def test_transferencia_debito_monto_bajo_sin_token():
    # Débito <= $5,000 no requiere token
    t = Transferencia(10000.0)
    exito, _ = t.procesar_transferencia(5000.0, 12, "Débito", token_activo=False)
    assert exito is True
    assert t.estado == "APROBADA"
    assert t.saldo_disponible == 5000.0

def test_transferencia_debito_monto_alto_con_token():
    # Débito > $5,000 con token_activo=True es aprobado
    t = Transferencia(10000.0)
    exito, _ = t.procesar_transferencia(5001.0, 12, "Débito", token_activo=True)
    assert exito is True
    assert t.estado == "APROBADA"
    assert t.saldo_disponible == 4999.0

def test_transferencia_debito_monto_alto_sin_token_rechazada():
    # Débito > $5,000 sin token_activo es rechazado
    t = Transferencia(10000.0)
    exito, _ = t.procesar_transferencia(5001.0, 12, "Débito", token_activo=False)
    assert exito is False
    assert t.estado == "RECHAZADA_POR_POLÍTICA"
    assert t.saldo_disponible == 10000.0


# 4. Validaciones de Parámetros Genéricos
def test_transferencia_parametros_invalidos():
    t = Transferencia(1000.0)
    # Monto negativo o cero
    exito1, _ = t.procesar_transferencia(0, 12, "Misma")
    assert exito1 is False
    exito2, _ = t.procesar_transferencia(-100, 12, "Misma")
    assert exito2 is False
    
    # Hora inválida
    exito3, _ = t.procesar_transferencia(100, 24, "Misma")
    assert exito3 is False
    exito4, _ = t.procesar_transferencia(100, -1, "Misma")
    assert exito4 is False

    # Cuenta destino no reconocida
    exito5, _ = t.procesar_transferencia(100, 12, "Desconocida")
    assert exito5 is False
