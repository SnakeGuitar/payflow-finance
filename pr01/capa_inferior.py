
TASA_ALTO_RIESGO_ANUAL = 0.12
TASA_BAJO_RIESGO_ANUAL = 0.05
ERROR_PLAZO_INVALIDO = "El plazo no puede ser menor a 1 año"
ERROR_CAPITAL_INVALIDO = "El capital a invertir no puede ser negativo"

def calcular_monto_alto_riesgo(capital: float, plazo_meses: float):
  return capital * (1 + TASA_ALTO_RIESGO_ANUAL) ** plazo_meses

def calcular_monto_bajo_riesgo(capital: float, plazo_meses: float):
  return capital * (1 + TASA_BAJO_RIESGO_ANUAL) ** plazo_meses

def obtener_errores_de_capa_inferior(es_alto_riesgo: bool, capital: float, plazo_meses: float):
  errores = {
    "error-plazo-invalido": None,
    "error-capital-invalido": None
  } 
  error = False

  if plazo_meses < 12:
    errores["error-plazo-invalido"] = ERROR_PLAZO_INVALIDO
    error = True

  if capital <= 0:
    errores["error-capital-invalido"] =  ERROR_CAPITAL_INVALIDO
    error = True

  if error:
    return errores

def calcular_monto(es_alto_riesgo: bool, capital: float, plazo_meses: float):
  errores = obtener_errores_de_capa_inferior(es_alto_riesgo, capital, plazo_meses)
  
  if errores != None:
    return [None, errores]
  
  return [calcular_monto_alto_riesgo(capital, plazo_meses) if es_alto_riesgo else calcular_monto_bajo_riesgo(capital, plazo_meses), None]