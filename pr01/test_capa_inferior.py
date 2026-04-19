from capa_inferior import calcular_monto, calcular_monto_alto_riesgo, calcular_monto_bajo_riesgo, ERROR_CAPITAL_INVALIDO, ERROR_PLAZO_INVALIDO

CAPITAL_VALIDO = 10_000
CAPITAL_NEGATIVO = -10_000
DURACION_MESES_VALIDO = 12
DURACION_MESES_INVALIDO = 6
PERFIL_ALTO_RIESGO = True
PERFIL_BAJO_RIESGO = False

def test_escenario_e1():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e2():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_VALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_escenario_e3():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e4():
  [inversion, errores] = calcular_monto(PERFIL_ALTO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_VALIDO)

  assert inversion == calcular_monto_alto_riesgo(CAPITAL_VALIDO, DURACION_MESES_VALIDO)
  assert errores == None

def test_escenario_e5():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e6():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_NEGATIVO, DURACION_MESES_VALIDO)

  assert inversion == None
  assert errores["error-capital-invalido"] == ERROR_CAPITAL_INVALIDO

def test_escenario_e7():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_INVALIDO)

  assert inversion == None
  assert errores["error-plazo-invalido"] == ERROR_PLAZO_INVALIDO

def test_escenario_e8():
  [inversion, errores] = calcular_monto(PERFIL_BAJO_RIESGO, CAPITAL_VALIDO, DURACION_MESES_VALIDO)

  assert inversion == calcular_monto_bajo_riesgo(CAPITAL_VALIDO, DURACION_MESES_VALIDO)
  assert errores == None