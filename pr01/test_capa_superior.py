from capa_superior import Payflow

SALDO = 12_000
DURACION_AÑOS_VALIDO = 1
CAPITAL_VALIDO = SALDO + 1
CAPITAL_INVALIDO = SALDO - 1
CAPITAL_INVALIDO_CERO = 0
DURACION_AÑOS_INVALIDO = 0.5
PERFIL_ALTO_RIESGO = True
PERFIL_BAJO_RIESGO = False
CUENTA_NUEVA = True
CUENTA_ANTIGUA = False

def test_escenario_e1():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_INVALIDO, DURACION_AÑOS_INVALIDO)

  assert folio == None
  assert errores != None  

def test_escenario_e2():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_VALIDO,  DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e3():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_INVALIDO, DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e4():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_INVALIDO, DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None