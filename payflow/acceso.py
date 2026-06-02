def validar_registro(edad: int, tiene_id: bool) -> str:
    return "ACCESO_CONCEDIDO" if edad >= 18 and tiene_id else "ACCESO_DENEGADO"
