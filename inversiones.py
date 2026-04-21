# Capa Inferior
from math import ceil

TASA_ALTO_RIESGO_ANUAL = 0.12
TASA_BAJO_RIESGO_ANUAL = 0.05
# Los errores para poder ser usados en las pruebas.
ERROR_PLAZO_INVALIDO = "El plazo no puede ser menor a 1 año"
ERROR_CAPITAL_INVALIDO = "El capital a invertir no puede ser negativo"

# Se separa la capa inferior en funciones pequeñas para poder probar cada una de ellas de forma independiente.
def calcular_monto_alto_riesgo(capital: float, plazo_meses: float):
  """
  Calcula el monto final de una inversión de alto riesgo.
  
  Aplica una tasa de interés anual de alto riesgo (12%) sobre el capital invertido.
  Basado en la fórmula: A = P(1 + r)^n.
  
  Args:
      capital (float): El capital inicial a invertir.
      plazo_meses (float): El plazo de la inversión en meses.
      
  Returns:
      int: El monto final calculado y redondeado hacia arriba.
  """
  return ceil(capital * (1 + TASA_ALTO_RIESGO_ANUAL) ** plazo_meses)

def calcular_monto_bajo_riesgo(capital: float, plazo_meses: float):
  """
  Calcula el monto final de una inversión de bajo riesgo.
  
  Aplica una tasa de interés anual de bajo riesgo (5%) sobre el capital invertido.
  Basado en la fórmula: A = P(1 + r)^n.
  
  Args:
      capital (float): El capital inicial a invertir.
      plazo_meses (float): El plazo de la inversión en meses.
      
  Returns:
      int: El monto final calculado y redondeado hacia arriba.
  """
  return ceil(capital * (1 + TASA_BAJO_RIESGO_ANUAL) ** plazo_meses)

def obtener_errores_de_capa_inferior(capital: float, plazo_meses: float):
  """
  Valida las condiciones base (capa inferior) para realizar una inversión.
  
  Verifica que el plazo de la inversión no sea menor a 1 año (12 meses) y que
  el capital a invertir no sea negativo ni cero.
  
  Args:
      capital (float): El monto del capital a invertir.
      plazo_meses (float): El plazo de la inversión en meses.
      
  Returns:
      dict | None: Un diccionario con los mensajes de error si las validaciones fallan,
      o None si los datos son válidos.
  """
  # Un diccionario con los errores de la capa inferior, si no hay errores, el valor de cada error es None.
  # Se usa un diccionario para poder agregar los errores de la capa superior en caso de que existan, sin perder los errores de la capa inferior.
  errores = {
    "error-plazo-invalido": None,
    "error-capital-invalido": None
  } 
  error = False

  if plazo_meses < 12:
    errores["error-plazo-invalido"] = ERROR_PLAZO_INVALIDO
    error = True

  if capital <= 0:
    errores["error-capital-invalido"] =  ERROR_CAPITAL_INVALIDO
    error = True

  if error:
    return errores

# La función principal de la capa inferior, que se encarga de calcular el monto a invertir, dependiendo del perfil de riesgo del cliente, el capital a invertir y el plazo en meses.
def calcular_monto(es_alto_riesgo: bool, capital: float, plazo_meses: float):
  """
  Calcula el monto de la inversión después de aplicar las validaciones de capa inferior.
  
  Valida las condiciones básicas del capital y el plazo. Si existen errores,
  devuelve la lista de errores. En caso contrario, calcula el rendimiento
  dependiendo de si el perfil es de alto o bajo riesgo.
  
  Args:
      es_alto_riesgo (bool): Indica si la inversión es de alto riesgo (True) o bajo riesgo (False).
      capital (float): El monto del capital a invertir.
      plazo_meses (float): El plazo de la inversión en meses.
      
  Returns:
      list: Una lista que contiene [monto_calculado, errores], donde uno de los dos es None.
  """
  errores = obtener_errores_de_capa_inferior(capital, plazo_meses)
  
  if errores != None:
    return [None, errores]
  
  return [calcular_monto_alto_riesgo(capital, plazo_meses) if es_alto_riesgo else calcular_monto_bajo_riesgo(capital, plazo_meses), None]

# Capa Media
ERROR_CUENTA_NUEVA = "No se permiten inversiones de alto riesgo para cuentas nuevas"
ERROR_CAPITAL_EXCEDIDO = "Rechazada por exceder el saldo disponible"

def generar_resultado(es_alto_riesgo: bool, capital: float, plazo_años: float, estado: str):
    """
    Genera el resultado de la inversión estructurado con el formato requerido.
    
    Formato del resultado aprobado: '<PERFIL>-<ESTADO>-<MONTO_FINAL>' 
    Ejemplo: 'A-R-1500' o 'B-E-1050'. 
    Si la inversión es rechazada por errores de validación, devuelve los errores.
    
    Args:
        es_alto_riesgo (bool): Perfil de la inversión (True=Alto, False=Bajo).
        capital (float): Capital a invertir.
        plazo_años (float): Plazo de la inversión.
        estado (str): El estado de la cuenta/inversión ("INVERSION_RIESGOSA" o "INVERSION_ESTABLE").
        
    Returns:
        list: Una lista [resultado_formateado, None] en caso de éxito, o [None, errores] en caso de fallo.
    """
    [inversion, errores] = calcular_monto(es_alto_riesgo, capital, plazo_años)
    
    if errores == None:
        return [f"{"A" if es_alto_riesgo else "B"}-{"R" if estado == "INVERSION_RIESGOSA" else "E"}-{int(inversion)}", None]
    
    return [None, errores]

# Capa Superior
def obtener_errores_de_capa_superior(es_alto_riesgo: bool, cuenta_nueva: bool, capital: float, saldo: float):
  """
  Valida las condiciones de negocio (capa superior) para autorizar una inversión.
  
  Verifica reglas de negocio específicas:
  1. Una cuenta nueva (menor a 3 meses) no puede optar por un perfil de alto riesgo.
  2. El capital a invertir no puede exceder el saldo disponible en la cuenta.
  
  Args:
      es_alto_riesgo (bool): Indica si la inversión es de alto riesgo.
      cuenta_nueva (bool): Indica si la cuenta del usuario es de reciente creación.
      capital (float): El monto de capital a invertir.
      saldo (float): El saldo actual de la cuenta.
      
  Returns:
      dict | None: Un diccionario con los mensajes de error correspondientes,
      o None si cumple con las validaciones de negocio.
  """
  # Un diccionario con los errores de la capa superior, si no hay errores, el valor de cada error es None.
  # Se usa un diccionario para poder agregar los errores de la capa inferior en caso de que existan, sin perder los errores de la capa superior.
  errores = {
    "error-cuenta-nueva": None,
    "error-capital-excedido": None,
  }
  error = False

  if es_alto_riesgo and cuenta_nueva:
    errores["error-cuenta-nueva"] = ERROR_CUENTA_NUEVA
    error = True

  if capital > saldo:
    errores["error-capital-excedido"] = ERROR_CAPITAL_EXCEDIDO
    error = True

  if error:
    return errores

class Payflow:
  """
  Clase principal que gestiona el estado y saldo de una cuenta Payflow para realizar inversiones.
  """
  estado = "DISPONIBLE"
  saldo = 0
  cuenta_nueva = False

  def __init__(self, saldo: float, cuenta_nueva: bool):
    """
    Inicializa una cuenta Payflow.
    
    Args:
        saldo (float): Saldo inicial disponible en la cuenta.
        cuenta_nueva (bool): Indica si la cuenta tiene menos de 3 meses de antigüedad.
    """
    self.saldo = saldo
    self.cuenta_nueva = cuenta_nueva
    
  def realizar_inversion(self, es_alto_riesgo: bool, capital: float, plazo_meses: float):
    """
    Procesa una solicitud de inversión evaluando todas las capas de validación y reglas de negocio.
    
    Orquesta el flujo completo de la inversión:
    1. Valida las reglas de negocio (capa superior).
    2. Valida las condiciones numéricas básicas (capa inferior).
    3. Determina el estado de la inversión según el monto arriesgado 
       (INVERSION_RIESGOSA si capital >= 50% del saldo, de lo contrario INVERSION_ESTABLE).
    4. Genera el folio de resultado o devuelve los errores encontrados.
    
    Args:
        es_alto_riesgo (bool): Indica si se elige perfil de alto riesgo (True) o bajo riesgo (False).
        capital (float): El capital que se desea invertir.
        plazo_meses (float): El tiempo de la inversión en meses.
        
    Returns:
        list: Lista con [folio_aprobacion, errores]. Retorna el folio si es aprobado o los errores si es rechazada.
    """
    errores = obtener_errores_de_capa_superior(es_alto_riesgo, self.cuenta_nueva, capital, self.saldo)

    if errores != None:
      errores_capa_inferior = obtener_errores_de_capa_inferior(capital, plazo_meses)
      
      if errores_capa_inferior != None:
        errores.update(errores_capa_inferior)

      self.estado = "RECHAZADA"
      return [None, errores]

    if capital >= self.saldo / 2:
      self.estado = "INVERSION_RIESGOSA"
    else:
      self.estado = "INVERSION_ESTABLE"

    return generar_resultado(es_alto_riesgo, capital, plazo_meses, self.estado)