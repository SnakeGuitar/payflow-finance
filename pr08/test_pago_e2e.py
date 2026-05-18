from payflow_pago import CuentaUsuario, Pago, PagoCapaInferior, PagoCapaSuperior

class TestE2E:
  @staticmethod
  def test_pago_exitoso():
    cuenta_usuario = CuentaUsuario("0", 5_000)
    SALDO_FINAL = PagoCapaInferior.calcular_nuevo_saldo(3_500, cuenta_usuario)
    [es_fallida, folio] = Pago.realizar_pago(3_500, cuenta_usuario, PagoCapaSuperior.CONCEPTOS["RENTA"])

    assert es_fallida == False
    assert folio.startswith("PAGO-RENTA")
    assert cuenta_usuario.saldo_disponible == SALDO_FINAL

  @staticmethod
  def test_pago_insuficiente():
    SALDO_INICIAL = 1_010
    cuenta_usuario = CuentaUsuario("0", SALDO_INICIAL)
    [es_fallida, folio] = Pago.realizar_pago(1000, cuenta_usuario, PagoCapaSuperior.CONCEPTOS["INTERNET"])

    assert es_fallida == True
    assert folio == None
    assert cuenta_usuario.saldo_disponible == SALDO_INICIAL

  @staticmethod
  def test_pago_concepto_invalido():
    SALDO_INICIAL = 1_010
    cuenta_usuario = CuentaUsuario("0", SALDO_INICIAL)
    [es_fallida, folio] = Pago.realizar_pago(1000, cuenta_usuario, "MÉXICO")

    assert es_fallida == True
    assert folio == None
    assert cuenta_usuario.saldo_disponible == SALDO_INICIAL