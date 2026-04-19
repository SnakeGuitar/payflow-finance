from capa_media import generar_resultado

class Payflow:
  estado = "DISPONIBLE"
  saldo = 0
  cuenta_nueva = False

  def __init__(self, saldo: float, cuenta_nueva: bool):
    self.saldo = saldo
    self.cuenta_nueva = cuenta_nueva
    
  def realizar_inversion(self, es_alto_riesgo: bool, capital: float, plazo_años: float):
    errores = {
      "error-cuenta-nueva": None,
      "error-capital-excedido": None,
      "error-plazo-invalido": None,
      "error-capital-invalido": None
    }

    if es_alto_riesgo and self.cuenta_nueva:
      self.estado = "RECHAZADA"
      errores["error-cuenta-nueva"] = "No se permiten inversiones de alto riesgo para cuentas nuevas"

    if capital > self.saldo:
      self.estado = "RECHAZADA"
      errores["error-capital-excedido"] = "Rechazada por exceder el saldo disponible"

    if plazo_años < 1:
      self.estado = "RECHAZADA"
      errores["error-plazo-invalido"] = "El plazo no puede ser menor a 1 año"

    if capital <= 0:
      self.estado = "RECHAZADA"
      errores["error-capital-invalido"] = "El capital a invertir no puede ser negativo"    

    if self.estado == "RECHAZADA":
      return [None, errores]

    if es_alto_riesgo:
      self.estado = "INVERSION_RIESGOSA"
    else:
      self.estado = "INVERSION_ESTABLE"

    return generar_resultado(es_alto_riesgo, capital, self.cuenta_nueva, plazo_años)