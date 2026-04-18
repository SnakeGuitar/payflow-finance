from capa_superior import Payflow

SALDO = 12_000
DURACION_AÑOS_VALIDO = 1
DURACION_AÑOS_INVALIDO = 0.5
CAPITAL_RIESGO = SALDO / 2
CAPITAL_RIESGO_ARRIBA = SALDO + 1
CAPITAL_INVALIDO = 0
PERFIL_ALTO_RIESGO = True
PERFIL_BAJO_RIESGO = False
CUENTA_NUEVA = True
CUENTA_ANTIGUA = False

def test_escenario_e1():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_AÑOS_INVALIDO)

  assert folio == None
  assert errores != None  

def test_escenario_e2():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA,  DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e3():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_AÑOS_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e4():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e5():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_AÑOS_INVALIDO)

  assert folio == None
  assert errores != None  

def test_escenario_e6():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_AÑOS_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e7():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_AÑOS_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e8():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_AÑOS_VALIDO)

  assert folio != None
  assert errores == None