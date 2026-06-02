class Transferencia:
    def __init__(self, saldo_disponible: float):
        self.saldo_disponible = saldo_disponible
        self.estado = "PENDIENTE"

    def _validar_monto_y_hora(self, monto: float, hora: int) -> str | None:
        if monto <= 0 or monto > self.saldo_disponible:
            return "Saldo insuficiente o monto de transferencia invalido."
        if hora < 0 or hora > 23:
            return "Hora de transferencia fuera del rango valido (0-23)."
        return None

    def _validar_credito(self, monto: float, hora: int, token_activo: bool) -> tuple[bool, str]:
        if not (9 <= hora <= 18):
            return False, "Transferencias a cuentas de tipo Credito solo se permiten de 09:00 a 18:00 hrs."
        return True, "Transferencia a credito aprobada exitosamente."

    def _validar_debito(self, monto: float, hora: int, token_activo: bool) -> tuple[bool, str]:
        if monto > 5000.0 and not token_activo:
            return False, "Transferencias a cuentas de tipo Debito mayores a $5,000 requieren token activo."
        return True, "Transferencia a debito aprobada exitosamente."

    def _validar_misma(self, monto: float, hora: int, token_activo: bool) -> tuple[bool, str]:
        return True, "Transferencia aprobada exitosamente."

    def procesar_transferencia(self, monto: float, hora: int, tipo_cuenta: str, token_activo: bool = False) -> tuple[bool, str]:
        self.estado = "PENDIENTE"

        err_msg = self._validar_monto_y_hora(monto, hora)
        if err_msg:
            self.estado = "RECHAZADA_POR_POLÍTICA"
            return False, err_msg

        validadores = {
            "Misma": self._validar_misma,
            "Crédito": self._validar_credito,
            "Débito": self._validar_debito
        }

        validador = validadores.get(tipo_cuenta)
        if not validador:
            self.estado = "RECHAZADA_POR_POLÍTICA"
            return False, "Tipo de cuenta destino no reconocido."

        exito, msg = validador(monto, hora, token_activo)
        if exito:
            self.estado = "APROBADA"
            self.saldo_disponible -= monto
        else:
            self.estado = "RECHAZADA_POR_POLÍTICA"
        return exito, msg
