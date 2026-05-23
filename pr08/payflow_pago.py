from time import time

class CuentaUsuario:
  id: str
  saldo_disponible: float

  def __init__(self, id: str, saldo_disponible: float):
    self.id = id
    self.saldo_disponible = saldo_disponible


class PagoCapaSuperior:
  CONCEPTOS = {
    "RENTA": "RENTA",
    "INTERNET": "INTERNET",
    "LUZ": "LUZ"
  }

  @staticmethod
  def es_pago_valido(monto: float, cuenta_usuario: CuentaUsuario, concepto: str) -> bool:
    if concepto == "INTERNET":
      return PagoCapaInferior.calcular_monto_sin_comision(monto) <= cuenta_usuario.saldo_disponible
    return PagoCapaInferior.calcular_monto_total(monto) <= cuenta_usuario.saldo_disponible
  
  @staticmethod
  def es_concepto_valido(concepto: str):
    return concepto in PagoCapaSuperior.CONCEPTOS
  

class PagoCapaInferior:
  COMISION_FIJA = 15.0

  @staticmethod
  def calcular_monto_total(monto_base: float) -> float:
    return monto_base + PagoCapaInferior.COMISION_FIJA

  @staticmethod
  def calcular_monto_sin_comision(monto_base: float) -> float:
    return monto_base

  @staticmethod
  def calcular_nuevo_saldo(monto_base: float, cuenta_usuario: CuentaUsuario) -> float:
    return cuenta_usuario.saldo_disponible - PagoCapaInferior.calcular_monto_total(monto_base)

  @staticmethod
  def calcular_nuevo_saldo_sin_comision(monto_base: float, cuenta_usuario: CuentaUsuario) -> float:
    return cuenta_usuario.saldo_disponible - PagoCapaInferior.calcular_monto_sin_comision(monto_base)
  

class PagoCapaMedia:
  def generar_comprobante_pago(concepto: str):
    return f"PAGO-{concepto}-{time()}"
  

class Pago:
  @staticmethod
  def realizar_pago(monto: float, cuenta_usuario: CuentaUsuario, concepto: str) -> tuple[bool, str]:
    if not PagoCapaSuperior.es_concepto_valido(concepto):
      return [True, None]
    
    if not PagoCapaSuperior.es_pago_valido(monto, cuenta_usuario, concepto):
      return [True, None]

    if concepto == "INTERNET":
      cuenta_usuario.saldo_disponible = PagoCapaInferior.calcular_nuevo_saldo_sin_comision(monto, cuenta_usuario)
      return [False, PagoCapaMedia.generar_comprobante_pago(concepto)]
    
    cuenta_usuario.saldo_disponible = PagoCapaInferior.calcular_nuevo_saldo(monto, cuenta_usuario)
    return [False, PagoCapaMedia.generar_comprobante_pago(concepto)]
    