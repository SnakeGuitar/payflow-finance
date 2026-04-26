class ValidadorInversión:
  PERFILES = {
    "RIESGOSO": "RIESGOSO",
    "CONSERVADOR": "CONSERVADOR"
  }
  ESTADOS = {
    "ACEPTADA": "ACEPTADA",
    "REVISIÓN": "REVISIÓN",
    "RECHAZADA": "RECHAZADA",
  }
  MONTO_IDEAL = 10_000
  PLAZO_LARGO_MINIMO_EN_MESES = 12

  @staticmethod
  def es_monto_ideal(monto: float) -> bool:
    return monto >= ValidadorInversión.MONTO_IDEAL

  @staticmethod
  def es_plazo_largo(plazo_meses: float) -> bool:
    return plazo_meses >= ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES

  @staticmethod
  def es_perfil_valido(perfil: str) -> bool:
    return perfil in ValidadorInversión.PERFILES

  @staticmethod
  def validar_inversión(monto: float, plazo_meses: float, perfil: str):
    pass

class TestPC01:
  PLAZO_CORTO_EN_MESES = 6

  @staticmethod
  def test_caso_de_prueba_01():
    assert ValidadorInversión.validar_inversión(
      ValidadorInversión.MONTO_IDEAL, 
      ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES, 
      ValidadorInversión.PERFILES["RIESGOSO"]
    ) == ValidadorInversión.ESTADOS["ACEPTADA"]

  @staticmethod
  def test_caso_de_prueba_02():
    assert ValidadorInversión.validar_inversión(
      ValidadorInversión.MONTO_IDEAL, 
      ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES, 
      ValidadorInversión.PERFILES["CONSERVADOR"]
    ) == ValidadorInversión.ESTADOS["ACEPTADA"]

  @staticmethod
  def test_caso_de_prueba_03():
    assert ValidadorInversión.validar_inversión(
      ValidadorInversión.MONTO_IDEAL, 
      TestPC01.PLAZO_CORTO_EN_MESES, 
      ValidadorInversión.PERFILES["RIESGOSO"]
    ) == ValidadorInversión.ESTADOS["ACEPTADA"]