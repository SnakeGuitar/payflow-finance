class Transferencia:
    def __init__(self, saldo_disponible: float):
        self.saldo_disponible = saldo_disponible
        self.estado = "PENDIENTE"

    def procesar_transferencia(self, monto: float, hora: int, tipo_cuenta: str, token_activo: bool = False) -> tuple[bool, str]:
        self.estado = "PENDIENTE"

        if monto <= 0 or monto > self.saldo_disponible:
            self.estado = "RECHAZADA_POR_POLÍTICA"
            return False, "Saldo insuficiente o monto de transferencia invalido."

        if hora < 0 or hora > 23:
            self.estado = "RECHAZADA_POR_POLÍTICA"
            return False, "Hora de transferencia fuera del rango valido (0-23)."

        if tipo_cuenta == "Misma":
            self.estado = "APROBADA"
            self.saldo_disponible -= monto
            return True, "Transferencia aprobada exitosamente."

        elif tipo_cuenta == "Crédito":
            if 9 <= hora <= 18:
                self.estado = "APROBADA"
                self.saldo_disponible -= monto
                return True, "Transferencia a credito aprobada exitosamente."
            else:
                self.estado = "RECHAZADA_POR_POLÍTICA"
                return False, "Transferencias a cuentas de tipo Credito solo se permiten de 09:00 a 18:00 hrs."

        elif tipo_cuenta == "Débito":
            if monto > 5000.0 and not token_activo:
                self.estado = "RECHAZADA_POR_POLÍTICA"
                return False, "Transferencias a cuentas de tipo Debito mayores a $5,000 requieren token activo."
            else:
                self.estado = "APROBADA"
                self.saldo_disponible -= monto
                return True, "Transferencia a debito aprobada exitosamente."

        else:
            self.estado = "RECHAZADA_POR_POLÍTICA"
            return False, "Tipo de cuenta destino no reconocido."
