from capa_media import generar_resultado
from capa_inferior import obtener_errores_de_capa_inferior

ERROR_CUENTA_NUEVA = "No se permiten inversiones de alto riesgo para cuentas nuevas"
ERROR_CAPITAL_EXCEDIDO = "Rechazada por exceder el saldo disponible"

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