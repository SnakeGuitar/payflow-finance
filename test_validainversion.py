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
    es_monto_ideal = ValidadorInversión.es_monto_ideal(monto)
    es_plazo_largo = ValidadorInversión.es_plazo_largo(plazo_meses)
    es_perfil_riesgoso = perfil == ValidadorInversión.PERFILES["RIESGOSO"]
    es_perfil_conservador = perfil == ValidadorInversión.PERFILES["CONSERVADOR"]

    if es_monto_ideal and es_perfil_riesgoso:
      return ValidadorInversión.ESTADOS["ACEPTADA"]
    
    if not es_monto_ideal and not es_plazo_largo:
      return ValidadorInversión.ESTADOS["RECHAZADA"]

    if es_perfil_conservador and es_monto_ideal:
      return ValidadorInversión.ESTADOS["ACEPTADA"] if es_plazo_largo else ValidadorInversión.ESTADOS["REVISIÓN"]


MONTO_NO_IDEAL = 5_000
PLAZO_CORTO_EN_MESES = 6

class TestPC01:
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
      PLAZO_CORTO_EN_MESES, 
      ValidadorInversión.PERFILES["RIESGOSO"]
    ) == ValidadorInversión.ESTADOS["ACEPTADA"]
  

class TestPC02:
  @staticmethod
  def test_caso_de_prueba_04():
    assert ValidadorInversión.validar_inversión(
      ValidadorInversión.MONTO_IDEAL, 
      PLAZO_CORTO_EN_MESES, 
      ValidadorInversión.PERFILES["CONSERVADOR"]
    ) == ValidadorInversión.ESTADOS["REVISIÓN"]

  @staticmethod
  def test_caso_de_prueba_05():
    assert ValidadorInversión.validar_inversión(
      MONTO_NO_IDEAL, 
      ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES, 
      ValidadorInversión.PERFILES["RIESGOSO"]
    ) == ValidadorInversión.ESTADOS["REVISIÓN"]


class TestPC03:
  @staticmethod
  def test_caso_de_prueba_06():
    assert ValidadorInversión.validar_inversión(
      MONTO_NO_IDEAL, 
      ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES, 
      ValidadorInversión.PERFILES["CONSERVADOR"]
    ) == ValidadorInversión.ESTADOS["RECHAZADA"]

  @staticmethod
  def test_caso_de_prueba_07():
    assert ValidadorInversión.validar_inversión(
      MONTO_NO_IDEAL, 
      PLAZO_CORTO_EN_MESES, 
      ValidadorInversión.PERFILES["RIESGOSO"]
    ) == ValidadorInversión.ESTADOS["RECHAZADA"]

  @staticmethod
  def test_caso_de_prueba_08():
    assert ValidadorInversión.validar_inversión(
      MONTO_NO_IDEAL, 
      PLAZO_CORTO_EN_MESES, 
      ValidadorInversión.PERFILES["CONSERVADOR"]
    ) == ValidadorInversión.ESTADOS["RECHAZADA"]