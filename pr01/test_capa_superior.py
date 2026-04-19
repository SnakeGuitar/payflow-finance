from capa_superior import Payflow

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
  assert errores != None  

def test_escenario_e2():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA,  DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e3():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e4():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e5():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None  

def test_escenario_e6():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e7():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e8():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None

def test_escenario_e9():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e10():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e11():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e12():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_ALTO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None

def test_escenario_e13():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e14():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e15():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e16():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO_ARRIBA, DURACION_MESES_VALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e17():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e18():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None

def test_escenario_e19():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e20():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_RIESGO, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None

def test_escenario_e21():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e22():
  payflow = Payflow(SALDO, CUENTA_NUEVA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None

def test_escenario_e23():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_INVALIDO)

  assert folio == None
  assert errores != None

def test_escenario_e24():
  payflow = Payflow(SALDO, CUENTA_ANTIGUA)
  [folio, errores] = payflow.realizar_inversion(PERFIL_BAJO_RIESGO, CAPITAL_ESTABLE, DURACION_MESES_VALIDO)

  assert folio != None
  assert errores == None