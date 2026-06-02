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
    def validar_inversión(monto: float, plazo_meses: float, perfil: str):
        if perfil not in ValidadorInversión.PERFILES:
            return ValidadorInversión.ESTADOS["RECHAZADA"]

        es_monto_ideal = ValidadorInversión.es_monto_ideal(monto)
        es_plazo_largo = ValidadorInversión.es_plazo_largo(plazo_meses)
        es_perfil_riesgoso = perfil == ValidadorInversión.PERFILES["RIESGOSO"]

        # Tabla de verdad mapeada directamente (Complejidad Ciclomática = 2)
        tabla_decision = {
            (True, True, True): ValidadorInversión.ESTADOS["ACEPTADA"],      # Ideal + Largo + Riesgoso
            (True, True, False): ValidadorInversión.ESTADOS["ACEPTADA"],     # Ideal + Largo + Conservador
            (True, False, True): ValidadorInversión.ESTADOS["ACEPTADA"],     # Ideal + Corto + Riesgoso
            (True, False, False): ValidadorInversión.ESTADOS["REVISIÓN"],    # Ideal + Corto + Conservador
            (False, True, True): ValidadorInversión.ESTADOS["REVISIÓN"],     # No Ideal + Largo + Riesgoso
            (False, True, False): ValidadorInversión.ESTADOS["RECHAZADA"],   # No Ideal + Largo + Conservador
            (False, False, True): ValidadorInversión.ESTADOS["RECHAZADA"],   # No Ideal + Corto + Riesgoso
            (False, False, False): ValidadorInversión.ESTADOS["RECHAZADA"]   # No Ideal + Corto + Conservador
        }

        key = (es_monto_ideal, es_plazo_largo, es_perfil_riesgoso)
        return tabla_decision.get(key, ValidadorInversión.ESTADOS["RECHAZADA"])
