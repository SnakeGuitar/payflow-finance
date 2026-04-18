from capa_media import generar_resultado

class Payflow:
  estado = "DISPONIBLE"
  saldo = 0
  cuenta_nueva = False

  def __init__(self, saldo: float, cuenta_nueva: bool):
    self.saldo = saldo
    self.cuenta_nueva = cuenta_nueva
    
  def realizar_inversion(self, es_alto_riesgo: bool, capital: float, cuenta_nueva: bool, plazo_años: float):
    return generar_resultado(es_alto_riesgo, capital, cuenta_nueva, plazo_años)