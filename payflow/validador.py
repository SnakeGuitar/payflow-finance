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
        if not ValidadorInversión.es_perfil_valido(perfil):
            return ValidadorInversión.ESTADOS["RECHAZADA"]

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

        if not es_monto_ideal and es_plazo_largo:
            return ValidadorInversión.ESTADOS["REVISIÓN"] if es_perfil_riesgoso else ValidadorInversión.ESTADOS["RECHAZADA"]

        return ValidadorInversión.ESTADOS["RECHAZADA"]
