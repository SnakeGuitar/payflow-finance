class SuscripcionStreaming:
    ESTADOS = {
        "INACTIVO": "INACTIVO",
        "ACTIVO": "ACTIVO",
        "MORA": "MORA",
        "SUSPENDIDO": "SUSPENDIDO",
        "CANCELADO": "CANCELADO"
    }
    TRANSICIONES = {
        "INACTIVO":   ["REGISTRO", "PAGO_EXITOSO", "CANCELACION"],
        "ACTIVO":     ["PAGO_EXITOSO", "PAGO_VENCIDO", "CANCELACION"],
        "MORA":       ["PAGO_EXITOSO", "PAGO_VENCIDO", "MORA_AGOTADA", "RECUPERACION", "CANCELACION"],
        "SUSPENDIDO": ["PAGO_EXITOSO", "PAGO_VENCIDO", "MORA_AGOTADA", "RECUPERACION", "CANCELACION"],
        "CANCELADO":  []
    }
    PERIODO_DE_GRACIA_EN_DIAS = 3

    @staticmethod
    def es_estado_valido(estado: str) -> bool:
        return estado in SuscripcionStreaming.ESTADOS
    
    @staticmethod
    def es_transicion_valida(estado_actual: str, transicion: str) -> bool:
        return transicion in SuscripcionStreaming.TRANSICIONES[estado_actual]


# ── Entradas ───────────────────────────────────────────────────────────────────
REGISTRO     = "REGISTRO"
PAGO_EXITOSO = "PAGO_EXITOSO"
PAGO_VENCIDO = "PAGO_VENCIDO"
MORA_AGOTADA = "MORA_AGOTADA"
RECUPERACION = "RECUPERACION"
CANCELACION  = "CANCELACION"


# ── PC01: Casos donde el resultado debe ser "ACCESO HABILITADO" ────────────────
class TestPC01:
    @staticmethod
    def test_caso_de_prueba_02():  # C2: Inactivo + Pago exitoso → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], PAGO_EXITOSO
        ) == True

    @staticmethod
    def test_caso_de_prueba_04():  # C4: Activo + Pago exitoso → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], PAGO_EXITOSO
        ) == True

    @staticmethod
    def test_caso_de_prueba_07():  # C7: Mora + Pago exitoso → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], PAGO_EXITOSO
        ) == True

    @staticmethod
    def test_caso_de_prueba_10():  # C10: Mora + Recuperación → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], RECUPERACION
        ) == True

    @staticmethod
    def test_caso_de_prueba_12():  # C12: Suspendido + Pago exitoso → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], PAGO_EXITOSO
        ) == True

    @staticmethod
    def test_caso_de_prueba_15():  # C15: Suspendido + Recuperación → Activo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], RECUPERACION
        ) == True


# ── PC02: Casos donde el resultado debe ser "ACCESO RESTRINGIDO" ───────────────
class TestPC02:
    @staticmethod
    def test_caso_de_prueba_01():  # C1: Inactivo + Registro → Inactivo
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], REGISTRO
        ) == True

    @staticmethod
    def test_caso_de_prueba_05():  # C5: Activo + Pago vencido → Mora
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], PAGO_VENCIDO
        ) == True

    @staticmethod
    def test_caso_de_prueba_08():  # C8: Mora + Pago vencido → Suspendido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], PAGO_VENCIDO
        ) == True

    @staticmethod
    def test_caso_de_prueba_09():  # C9: Mora + Mora agotada → Suspendido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], MORA_AGOTADA
        ) == True

    @staticmethod
    def test_caso_de_prueba_13():  # C13: Suspendido + Pago vencido → Suspendido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], PAGO_VENCIDO
        ) == True

    @staticmethod
    def test_caso_de_prueba_14():  # C14: Suspendido + Mora agotada → Suspendido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], MORA_AGOTADA
        ) == True


# ── PC03: Casos donde el resultado debe ser "CANCELACIÓN CONFIRMADA" ───────────
class TestPC03:
    @staticmethod
    def test_caso_de_prueba_03():  # C3: Inactivo + Cancelación → Cancelado
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], CANCELACION
        ) == True

    @staticmethod
    def test_caso_de_prueba_06():  # C6: Activo + Cancelación → Cancelado
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], CANCELACION
        ) == True

    @staticmethod
    def test_caso_de_prueba_11():  # C11: Mora + Cancelación → Cancelado
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], CANCELACION
        ) == True

    @staticmethod
    def test_caso_de_prueba_16():  # C16: Suspendido + Cancelación → Cancelado
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], CANCELACION
        ) == True


# ── PC04: Casos donde el resultado debe ser "RECHAZADA" ───────────────────────
class TestPC04:
    @staticmethod
    def test_caso_de_prueba_17():  # C17: Inactivo + Pago vencido → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], PAGO_VENCIDO
        ) == False

    @staticmethod
    def test_caso_de_prueba_18():  # C18: Inactivo + Mora agotada → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], MORA_AGOTADA
        ) == False

    @staticmethod
    def test_caso_de_prueba_19():  # C19: Inactivo + Recuperación → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["INACTIVO"], RECUPERACION
        ) == False

    @staticmethod
    def test_caso_de_prueba_20():  # C20: Activo + Registro → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], REGISTRO
        ) == False

    @staticmethod
    def test_caso_de_prueba_21():  # C21: Activo + Mora agotada → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], MORA_AGOTADA
        ) == False

    @staticmethod
    def test_caso_de_prueba_22():  # C22: Activo + Recuperación → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["ACTIVO"], RECUPERACION
        ) == False

    @staticmethod
    def test_caso_de_prueba_23():  # C23: Mora + Registro → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["MORA"], REGISTRO
        ) == False

    @staticmethod
    def test_caso_de_prueba_24():  # C24: Suspendido + Registro → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["SUSPENDIDO"], REGISTRO
        ) == False

    @staticmethod
    def test_caso_de_prueba_25():  # C25: Cancelado + Registro → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], REGISTRO
        ) == False

    @staticmethod
    def test_caso_de_prueba_26():  # C26: Cancelado + Pago exitoso → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], PAGO_EXITOSO
        ) == False

    @staticmethod
    def test_caso_de_prueba_27():  # C27: Cancelado + Pago vencido → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], PAGO_VENCIDO
        ) == False

    @staticmethod
    def test_caso_de_prueba_28():  # C28: Cancelado + Mora agotada → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], MORA_AGOTADA
        ) == False

    @staticmethod
    def test_caso_de_prueba_29():  # C29: Cancelado + Recuperación → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], RECUPERACION
        ) == False

    @staticmethod
    def test_caso_de_prueba_30():  # C30: Cancelado + Cancelación → inválido
        assert SuscripcionStreaming.es_transicion_valida(
            SuscripcionStreaming.ESTADOS["CANCELADO"], CANCELACION
        ) == False
