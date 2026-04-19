from capa_media import generar_resultado

class Payflow:
  estado = "DISPONIBLE"
  saldo = 0
  cuenta_nueva = False

  def __init__(self, saldo: float, cuenta_nueva: bool):
    self.saldo = saldo
    self.cuenta_nueva = cuenta_nueva
    
  def realizar_inversion(self, es_alto_riesgo: bool, capital: float, plazo_meses: float):
    errores = {
      "error-cuenta-nueva": None,
      "error-capital-excedido": None,
    }

    if es_alto_riesgo and self.cuenta_nueva:
      self.estado = "RECHAZADA"
      errores["error-cuenta-nueva"] = "No se permiten inversiones de alto riesgo para cuentas nuevas"

    if capital > self.saldo:
      self.estado = "RECHAZADA"
      errores["error-capital-excedido"] = "Rechazada por exceder el saldo disponible"

    if self.estado == "RECHAZADA":
      return [None, errores]

    if es_alto_riesgo:
      self.estado = "INVERSION_RIESGOSA"
    else:
      self.estado = "INVERSION_ESTABLE"

    return generar_resultado(es_alto_riesgo, capital, plazo_meses, self.estado)