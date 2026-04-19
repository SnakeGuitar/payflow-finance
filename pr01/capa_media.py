from capa_inferior import calcular_monto 

def generar_resultado(es_alto_riesgo: bool, capital: float, plazo_años: float, estado: str):
    [inversion, errores] = calcular_monto(es_alto_riesgo, capital, plazo_años)
    
    if errores == None:
        return [f"{"A" if es_alto_riesgo else "B"}-{"R" if estado == "INVERSION_RIESGOSA" else "E"}-{int(inversion)}", None]
    
    return [None, errores]