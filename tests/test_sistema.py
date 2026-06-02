import os
import pytest
import json
from payflow.sistema import SistemaPayflow

TEMP_DB_PATH = "payflow_db_test.json"

@pytest.fixture
def clean_db():
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)
    
    sistema = SistemaPayflow(db_path=TEMP_DB_PATH)
    yield sistema
    
    if os.path.exists(TEMP_DB_PATH):
        os.remove(TEMP_DB_PATH)

def test_inicializacion_db(clean_db):
    sistema = clean_db
    usuarios = sistema.obtener_usuarios()
    assert "Alice" in usuarios
    assert "Bob" in usuarios
    assert "Charlie" in usuarios

def test_crear_usuario(clean_db):
    sistema = clean_db
    exito, err = sistema.crear_usuario("David", 5000.0, False)
    assert exito is True
    assert err is None
    
    user = sistema.obtener_usuario("David")
    assert user is not None
    assert user["saldo_disponible"] == 5000.0
    assert user["cuenta_nueva"] is False

    exito, err = sistema.crear_usuario("David", 1000.0, False)
    assert exito is False
    assert err is not None

def test_crear_usuario_acceso_denegado(clean_db):
    sistema = clean_db
    # Intento de menor de edad
    exito, err = sistema.crear_usuario("Minor", 1000.0, False, edad=17, tiene_id=True)
    assert exito is False
    assert "ACCESO_DENEGADO" in err
    
    # Intento sin ID
    exito, err = sistema.crear_usuario("NoID", 1000.0, False, edad=20, tiene_id=False)
    assert exito is False
    assert "ACCESO_DENEGADO" in err

def test_pago_servicio_internet_sin_comision(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 1000.0, False)
    
    exito, folio, saldo = sistema.realizar_pago_servicio("TestUser", 200.0, "INTERNET")
    assert exito is True
    assert folio.startswith("PAGO-INTERNET-")
    assert saldo == 800.0

def test_pago_servicio_luz_con_comision(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 1000.0, False)
    
    exito, folio, saldo = sistema.realizar_pago_servicio("TestUser", 200.0, "LUZ")
    assert exito is True
    assert folio.startswith("PAGO-LUZ-")
    assert saldo == 785.0

def test_pago_servicio_saldo_insuficiente(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 100.0, False)
    
    exito, err, saldo = sistema.realizar_pago_servicio("TestUser", 90.0, "RENTA")
    assert exito is False
    assert "Saldo insuficiente" in err
    assert saldo == 100.0

def test_inversion_alto_riesgo_cuenta_antigua_aprobada(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 20000.0, False)
    
    exito, folio, saldo = sistema.realizar_inversion("TestUser", True, 10000.0, 12.0)
    assert exito is True
    assert folio.startswith("A-R-")
    assert saldo == 10000.0

def test_inversion_alto_riesgo_cuenta_nueva_rechazada(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 20000.0, True)
    
    exito, errores, saldo = sistema.realizar_inversion("TestUser", True, 5000.0, 12.0)
    assert exito is False
    assert "error-cuenta-nueva" in errores
    assert saldo == 20000.0

def test_inversion_bajo_riesgo_cuenta_nueva_aprobada(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 20000.0, True)
    
    exito, folio, saldo = sistema.realizar_inversion("TestUser", False, 5000.0, 12.0)
    assert exito is True
    assert folio.startswith("B-E-")
    assert saldo == 15000.0

def test_validar_inversion_perfil(clean_db):
    sistema = clean_db
    dictamen = sistema.validar_inversion(10000.0, 12.0, "RIESGOSO")
    assert dictamen == "ACEPTADA"
    
    dictamen = sistema.validar_inversion(5000.0, 6.0, "CONSERVADOR")
    assert dictamen == "RECHAZADA"

def test_streaming_suscripcion_flujo_exitoso(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 500.0, False)
    assert sistema.obtener_usuario("TestUser")["suscripcion_estado"] == "INACTIVO"

    exito, msg, estado = sistema.procesar_evento_suscripcion("TestUser", "PAGO_EXITOSO")
    assert exito is True
    assert estado == "ACTIVO"
    assert sistema.obtener_usuario("TestUser")["saldo_disponible"] == 350.0

    exito, msg, estado = sistema.procesar_evento_suscripcion("TestUser", "PAGO_VENCIDO")
    assert exito is True
    assert estado == "MORA"

    exito, msg, estado = sistema.procesar_evento_suscripcion("TestUser", "CANCELACION")
    assert exito is True
    assert estado == "CANCELADO"

def test_streaming_suscripcion_transicion_invalida(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 500.0, False)
    
    sistema.procesar_evento_suscripcion("TestUser", "CANCELACION")
    
    exito, msg, estado = sistema.procesar_evento_suscripcion("TestUser", "REGISTRO")
    assert exito is False
    assert "Transicion invalida" in msg
    assert estado == "CANCELADO"

def test_streaming_suscripcion_saldo_insuficiente(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 50.0, False)
    
    exito, msg, estado = sistema.procesar_evento_suscripcion("TestUser", "PAGO_EXITOSO")
    assert exito is False
    assert "saldo insuficiente" in msg
    assert estado == "INACTIVO"
    assert sistema.obtener_usuario("TestUser")["saldo_disponible"] == 50.0

def test_sistema_realizar_transferencia_exitosa(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 10000.0, False)
    
    # Transferencia Crédito en horario permitido
    exito, msg, saldo = sistema.realizar_transferencia("TestUser", 2000.0, 10, "Crédito")
    assert exito is True
    assert saldo == 8000.0
    
    user = sistema.obtener_usuario("TestUser")
    assert len(user.get("transferencias", [])) == 1
    assert user["transferencias"][0]["monto"] == 2000.0
    assert user["transferencias"][0]["estado"] == "APROBADA"

def test_sistema_realizar_transferencia_fallida(clean_db):
    sistema = clean_db
    sistema.crear_usuario("TestUser", 1000.0, False)
    
    # Transferencia Crédito en horario no permitido (ej: 8 AM)
    exito, msg, saldo = sistema.realizar_transferencia("TestUser", 200.0, 8, "Crédito")
    assert exito is False
    assert saldo == 1000.0
    assert "permiten de 09:00 a 18:00" in msg
