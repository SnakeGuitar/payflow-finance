from payflow.validador import ValidadorInversión

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


class TestEXP01:
  @staticmethod
  def test_caso_de_prueba_01():
    assert ValidadorInversión.validar_inversión(
      ValidadorInversión.MONTO_IDEAL, 
      ValidadorInversión.PLAZO_LARGO_MINIMO_EN_MESES, 
      "PERFIL DESCONOCIDO"
    ) == ValidadorInversión.ESTADOS["RECHAZADA"]
