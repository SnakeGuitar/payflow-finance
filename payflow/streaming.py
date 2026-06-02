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
        if not SuscripcionStreaming.es_estado_valido(estado_actual):
            return False
        return transicion in SuscripcionStreaming.TRANSICIONES[estado_actual]

# Entradas
REGISTRO     = "REGISTRO"
PAGO_EXITOSO = "PAGO_EXITOSO"
PAGO_VENCIDO = "PAGO_VENCIDO"
MORA_AGOTADA = "MORA_AGOTADA"
RECUPERACION = "RECUPERACION"
CANCELACION  = "CANCELACION"
