from capa_inferior import calcular_monto 

def generar_resultado(es_alto_riesgo: bool, capital: float, plazo_años: float, estado: str):
    monto_final = calcular_monto(es_alto_riesgo, capital, plazo_años)
    return [f"{"A" if es_alto_riesgo else "B"}-{"R" if estado == "INVERSION_RIESGOSA" else "INVERSION_ESTABLE"}-{int(monto_final)}", None]