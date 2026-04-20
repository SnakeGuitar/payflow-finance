# Capa Inferior
from math import ceil

TASA_ALTO_RIESGO_ANUAL = 0.12
TASA_BAJO_RIESGO_ANUAL = 0.05
ERROR_PLAZO_INVALIDO = "El plazo no puede ser menor a 1 año"
ERROR_CAPITAL_INVALIDO = "El capital a invertir no puede ser negativo"

def calcular_monto_alto_riesgo(capital: float, plazo_meses: float):
  return ceil(capital * (1 + TASA_ALTO_RIESGO_ANUAL) ** plazo_meses)

def calcular_monto_bajo_riesgo(capital: float, plazo_meses: float):
  return ceil(capital * (1 + TASA_BAJO_RIESGO_ANUAL) ** plazo_meses)

def obtener_errores_de_capa_inferior(capital: float, plazo_meses: float):
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
  errores = obtener_errores_de_capa_inferior(capital, plazo_meses)
  
  if errores != None:
    return [None, errores]
  
  return [calcular_monto_alto_riesgo(capital, plazo_meses) if es_alto_riesgo else calcular_monto_bajo_riesgo(capital, plazo_meses), None]

# Capa Media
ERROR_CUENTA_NUEVA = "No se permiten inversiones de alto riesgo para cuentas nuevas"
ERROR_CAPITAL_EXCEDIDO = "Rechazada por exceder el saldo disponible"

def generar_resultado(es_alto_riesgo: bool, capital: float, plazo_años: float, estado: str):
    [inversion, errores] = calcular_monto(es_alto_riesgo, capital, plazo_años)
    
    if errores == None:
        return [f"{"A" if es_alto_riesgo else "B"}-{"R" if estado == "INVERSION_RIESGOSA" else "E"}-{int(inversion)}", None]
    
    return [None, errores]

# Capa Superior
def obtener_errores_de_capa_superior(es_alto_riesgo: bool, cuenta_nueva: bool, capital: float, saldo: float):
  errores = {
    "error-cuenta-nueva": None,
    "error-capital-excedido": None,
  }
  error = False

  if es_alto_riesgo and cuenta_nueva:
    errores["error-cuenta-nueva"] = ERROR_CUENTA_NUEVA
    error = True

  if capital > saldo:
    errores["error-capital-excedido"] = ERROR_CAPITAL_EXCEDIDO
    error = True

  if error:
    return errores

class Payflow:
  estado = "DISPONIBLE"
  saldo = 0
  cuenta_nueva = False

  def __init__(self, saldo: float, cuenta_nueva: bool):
    self.saldo = saldo
    self.cuenta_nueva = cuenta_nueva
    
  def realizar_inversion(self, es_alto_riesgo: bool, capital: float, plazo_meses: float):
    errores = obtener_errores_de_capa_superior(es_alto_riesgo, self.cuenta_nueva, capital, self.saldo)

    if errores != None:
      errores_capa_inferior = obtener_errores_de_capa_inferior(capital, plazo_meses)
      
      if errores_capa_inferior != None:
        errores.update(errores_capa_inferior)

      return [None, errores]

    if capital >= self.saldo / 2:
      self.estado = "INVERSION_RIESGOSA"
    else:
      self.estado = "INVERSION_ESTABLE"

    return generar_resultado(es_alto_riesgo, capital, plazo_meses, self.estado)