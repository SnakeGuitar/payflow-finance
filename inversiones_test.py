from inversiones import Payflow, ERROR_CUENTA_NUEVA, ERROR_CAPITAL_EXCEDIDO
from inversiones import calcular_monto, calcular_monto_alto_riesgo, calcular_monto_bajo_riesgo, ERROR_PLAZO_INVALIDO, ERROR_CAPITAL_INVALIDO

# Test General
SALDO = 12_000
DURACION_MESES_VALIDO = 12
DURACION_MESES_INVALIDO = 6
CAPITAL_RIESGO = SALDO / 2
CAPITAL_RIESGO_ARRIBA = SALDO + 1
CAPITAL_ESTABLE = SALDO / 4
CAPITAL_INVALIDO = 0
PERFIL_ALTO_RIESGO = True
PERFIL_BAJO_RIESGO = False
CUENTA_NUEVA = True
CUENTA_ANTIGUA = False

def test_escenario_e1():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO
  assert errores["error-capital-invalido"] == None

def test_escenario_e2():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA,  DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA

def test_escenario_e3():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO  

def test_escenario_e4():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO

def test_escenario_e5():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e6():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA

def test_escenario_e7():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO
  
def test_escenario_e8():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  inversion = calcular_monto_alto_riesgo(CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio == f"A-R-{int(inversion)}"
  assert errores == None

def test_escenario_e9():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_INVALIDO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_escenario_e10():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-cuenta-nueva"] == ERROR_CUENTA_NUEVA

def test_escenario_e11():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_INVALIDO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  
def test_escenario_e12():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  inversion = calcular_monto_alto_riesgo(CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio == f"A-E-{int(inversion)}"
  assert errores == None

def test_escenario_e13():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e14():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO

def test_escenario_e15():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e16():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores["error-capital-excedido"] == ERROR_CAPITAL_EXCEDIDO

def test_escenario_e17():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e18():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  inversion = calcular_monto_bajo_riesgo(CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio == f"B-R-{int(inversion)}"
  assert errores == None

def test_escenario_e19():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e20():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  inversion = calcular_monto_bajo_riesgo(CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio == f"B-R-{int(inversion)}"
  assert errores == None

def test_escenario_e21():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_INVALIDO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_escenario_e22():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  inversion = calcular_monto_bajo_riesgo(CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio == f"B-E-{int(inversion)}"
  assert errores == None

def test_escenario_e23():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_INVALIDO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e24():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  inversion = calcular_monto_bajo_riesgo(CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio == f"B-E-{int(inversion)}"
  assert errores == None


# Test Capa Inferior

CAPITAL_VALIDO = 10_000
CAPITAL_NEGATIVO = -10_000

def test_capa_inferior_escenario_e1():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_capa_inferior_escenario_e2():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_VALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_capa_inferior_escenario_e3():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_capa_inferior_escenario_e4():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_VALIDO)

  assert inversion == calcular_monto_alto_riesgo(CAPITAL_VALIDO, DURACION_MESES_VALIDO)
  assert errores == None

def test_capa_inferior_escenario_e5():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_capa_inferior_escenario_e6():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_VALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_capa_inferior_escenario_e7():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_capa_inferior_escenario_e8():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_VALIDO)

  assert inversion == calcular_monto_bajo_riesgo(CAPITAL_VALIDO, DURACION_MESES_VALIDO)
  assert errores == None