from payflow.acceso import validar_registro

def test_validar_registro_exitoso():
    # Edad >= 18 Y tiene_id = True -> ACCESO_CONCEDIDO
    assert validar_registro(18, True) == "ACCESO_CONCEDIDO"
    assert validar_registro(25, True) == "ACCESO_CONCEDIDO"

def test_validar_registro_menor_de_edad():
    # Edad < 18 -> ACCESO_DENEGADO
    assert validar_registro(17, True) == "ACCESO_DENEGADO"
    assert validar_registro(10, True) == "ACCESO_DENEGADO"

def test_validar_registro_sin_identificacion():
    # tiene_id = False -> ACCESO_DENEGADO
    assert validar_registro(18, False) == "ACCESO_DENEGADO"
    assert validar_registro(25, False) == "ACCESO_DENEGADO"

def test_validar_registro_menor_y_sin_identificacion():
    # Edad < 18 Y tiene_id = False -> ACCESO_DENEGADO
    assert validar_registro(16, False) == "ACCESO_DENEGADO"
