import os
import sys
from payflow.sistema import SistemaPayflow

# Inicializacion de la consola para soporte ANSI en Windows
os.system('color')

# Codigos de colores ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_header(titulo):
    ancho = 62
    print(f"\n{BLUE}+" + "=" * (ancho - 2) + "+")
    # Centrar titulo
    pad = (ancho - 2 - len(titulo)) // 2
    pad_extra = (ancho - 2 - len(titulo)) % 2
    print(f"|" + " " * pad + f"{BOLD}{CYAN}{titulo}{RESET}{BLUE}" + " " * (pad + pad_extra) + "|")
    print("+" + "=" * (ancho - 2) + "+" + RESET)

def imprimir_dashboard(sistema, usuario_actual):
    if not usuario_actual:
        print(f"\n{YELLOW}[!] No hay ninguna cuenta seleccionada. Seleccione la opcion [1] primero.{RESET}")
        return

    user = sistema.obtener_usuario(usuario_actual)
    if not user:
        return

    antiguedad = f"{GREEN}Antigua (>= 3m){RESET}" if not user["cuenta_nueva"] else f"{YELLOW}Nueva (< 3m){RESET}"
    
    # Colorear suscripcion
    sub_color = GREEN if user["suscripcion_estado"] == "ACTIVO" else (YELLOW if user["suscripcion_estado"] in ["MORA", "SUSPENDIDO"] else RED)
    suscripcion = f"{sub_color}{user['suscripcion_estado']}{RESET}"

    print(f"\n{BLUE}+------------------------- INFORMACION DEL USUARIO -------------------------+")
    print(f"  {BOLD}Usuario:{RESET} {user['id']:<15} | {BOLD}Saldo Disponible:{RESET} {GREEN}${user['saldo_disponible']:,.2f}{RESET}")
    print(f"  {BOLD}Antiguedad:{RESET} {antiguedad:<24} | {BOLD}Estado Suscripcion:{RESET} {suscripcion}")
    print(f"{BLUE}+---------------------------------------------------------------------------+{RESET}")

def menu_usuario(sistema):
    imprimir_header("SELECCIONAR / CREAR CUENTA")
    usuarios = sistema.obtener_usuarios()
    
    print(f"\n{BOLD}Cuentas existentes:{RESET}")
    for i, u in enumerate(usuarios, 1):
        user = sistema.obtener_usuario(u)
        print(f"  {CYAN}[{i}]{RESET} {u} (Saldo: ${user['saldo_disponible']:,.2f})")
    
    print(f"  {GREEN}[N]{RESET} Crear nueva cuenta de usuario")
    print(f"  {RED}[R]{RESET} Regresar al menu principal")

    opcion = input(f"\n{BOLD}Seleccione una opcion: {RESET}").strip().upper()
    
    if opcion == 'R':
        return None
    
    if opcion == 'N':
        limpiar_pantalla()
        imprimir_header("CREAR NUEVO USUARIO")
        nuevo_id = input(f"{BOLD}Nombre del usuario / ID: {RESET}").strip()
        if not nuevo_id:
            print(f"{RED}[X] El nombre no puede estar vacio.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return None
        
        try:
            saldo = float(input(f"{BOLD}Saldo inicial disponible: ${RESET}"))
        except ValueError:
            print(f"{RED}[X] Saldo invalido.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return None

        antiguedad_resp = input(f"{BOLD}¿Es cuenta nueva (< 3 meses de antiguedad)? (S/N): {RESET}").strip().upper()
        es_nueva = True if antiguedad_resp == 'S' else False

        try:
            edad = int(input(f"{BOLD}Edad del usuario: {RESET}"))
        except ValueError:
            print(f"{RED}[X] Edad invalida.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return None

        id_resp = input(f"{BOLD}¿Posee identificacion oficial valida? (S/N): {RESET}").strip().upper()
        tiene_id = True if id_resp == 'S' else False

        exito, err = sistema.crear_usuario(nuevo_id, saldo, es_nueva, edad, tiene_id)
        if exito:
            print(f"\n{GREEN}[OK] Usuario '{nuevo_id}' creado exitosamente.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return nuevo_id
        else:
            print(f"\n{RED}[X] Error: {err}{RESET}")
            input(f"\nPresione Enter para continuar...")
            return None

    try:
        idx = int(opcion) - 1
        if 0 <= idx < len(usuarios):
            selected = usuarios[idx]
            print(f"\n{GREEN}[OK] Sesion iniciada como '{selected}'.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return selected
        else:
            print(f"{RED}[X] Opcion fuera de rango.{RESET}")
    except ValueError:
        print(f"{RED}[X] Entrada no valida.{RESET}")

    input(f"\nPresione Enter para continuar...")
    return None

def menu_pago_servicio(sistema, usuario_actual):
    if not usuario_actual:
        print(f"\n{RED}[X] Debe seleccionar un usuario primero.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    limpiar_pantalla()
    imprimir_dashboard(sistema, usuario_actual)
    imprimir_header("PAGO DE SERVICIOS (RENTA, INTERNET, LUZ)")

    print(f"\n{BOLD}Seleccione el concepto del servicio:{RESET}")
    print(f"  {CYAN}[1]{RESET} RENTA     (Aplica comision fija de $15.00)")
    print(f"  {CYAN}[2]{RESET} LUZ       (Aplica comision fija de $15.00)")
    print(f"  {CYAN}[3]{RESET} INTERNET  (Descuento especial: comision fija de $0.00)")
    print(f"  {RED}[R]{RESET} Cancelar y regresar")

    op = input(f"\n{BOLD}Seleccione una opcion: {RESET}").strip().upper()

    if op == 'R':
        return

    conceptos_map = {'1': "RENTA", '2': "LUZ", '3': "INTERNET"}
    concepto = conceptos_map.get(op)
    if not concepto:
        print(f"{RED}[X] Opcion invalida.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    try:
        monto = float(input(f"{BOLD}Ingrese el monto base a pagar: ${RESET}"))
        if monto <= 0:
            print(f"{RED}[X] El monto debe ser mayor a 0.{RESET}")
            input(f"\nPresione Enter para continuar...")
            return
    except ValueError:
        print(f"{RED}[X] Monto no valido.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    # Mostrar previsualizacion
    comision = 0.0 if concepto == "INTERNET" else 15.0
    total = monto + comision
    print(f"\n{BOLD}Detalle del Cobro:{RESET}")
    print(f"  Monto base:   ${monto:.2f}")
    print(f"  Comision:     ${comision:.2f} ({'Descuento Promocional' if concepto == 'INTERNET' else 'Tarifa Estandar'})")
    print(f"  Total a pagar: {BOLD}${total:.2f}{RESET}")

    confirm = input(f"\n{BOLD}¿Confirmar pago? (S/N): {RESET}").strip().upper()
    if confirm != 'S':
        print(f"{YELLOW}Pago cancelado por el usuario.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    exito, folio_o_err, saldo_act = sistema.realizar_pago_servicio(usuario_actual, monto, concepto)
    if exito:
        print(f"\n{GREEN}[OK] ¡Pago realizado con exito!{RESET}")
        print(f"  {BOLD}Folio de Comprobante:{RESET} {folio_o_err}")
        print(f"  {BOLD}Nuevo Saldo Disponible:{RESET} ${saldo_act:,.2f}")
    else:
        print(f"\n{RED}[X] Error al procesar pago: {folio_o_err}{RESET}")

    input(f"\nPresione Enter para continuar...")

def menu_inversiones(sistema, usuario_actual):
    if not usuario_actual:
        print(f"\n{RED}[X] Debe seleccionar un usuario primero.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    user = sistema.obtener_usuario(usuario_actual)
    if not user:
        return

    limpiar_pantalla()
    imprimir_dashboard(sistema, usuario_actual)
    imprimir_header("SIMULADOR Y REGISTRO DE INVERSIONES")

    print(f"\n{BOLD}Paso 1: Parametros de Inversion{RESET}")
    try:
        capital = float(input(f"  Monto del Capital a Invertir: ${RESET}"))
        plazo = float(input(f"  Plazo en Meses: {RESET}"))
    except ValueError:
        print(f"\n{RED}[X] Datos numericos invalidos.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    print(f"\n{BOLD}Paso 2: Perfil de Riesgo{RESET}")
    print(f"  {CYAN}[1]{RESET} ALTO RIESGO   (Tasa del 12% anual. Compuesto mensual. Req. cuenta antigua)")
    print(f"  {CYAN}[2]{RESET} BAJO RIESGO   (Tasa del 5% anual. Compuesto mensual. Acepta cuenta nueva)")
    riesgo_op = input(f"\nSeleccione perfil: ").strip()

    if riesgo_op not in ['1', '2']:
        print(f"{RED}[X] Opcion invalida.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    es_alto_riesgo = (riesgo_op == '1')
    perfil_validador = "RIESGOSO" if es_alto_riesgo else "CONSERVADOR"

    # 1. Validar Perfil de Inversion en Capa Validador
    dictamen = sistema.validar_inversion(capital, plazo, perfil_validador)
    
    dictamen_colors = {
        "ACEPTADA": f"{GREEN}{BOLD}ACEPTADA (Cumple condiciones ideales){RESET}",
        "REVISION": f"{YELLOW}{BOLD}REVISION (Sujeta a evaluacion intermedia){RESET}",
        "RECHAZADA": f"{RED}{BOLD}RECHAZADA (No cumple montos o plazos minimos){RESET}"
    }

    print(f"\n{BOLD}Resultados del Simulador & Pre-validacion:{RESET}")
    print(f"  - Calificacion de Perfil: {dictamen_colors.get(dictamen, dictamen)}")

    # 2. Correr la logica del motor para ver rendimientos esperados o errores
    from payflow.inversiones import calcular_monto_alto_riesgo, calcular_monto_bajo_riesgo
    
    estimado = None
    if capital > 0 and plazo >= 12:
        if es_alto_riesgo:
            estimado = calcular_monto_alto_riesgo(capital, plazo)
        else:
            estimado = calcular_monto_bajo_riesgo(capital, plazo)
        
        print(f"  - Rendimiento Estimado al final del plazo: {GREEN}${estimado:,.2f}{RESET} (Ganancia: +${estimado - capital:,.2f})")
    else:
        print(f"  - {YELLOW}Advertencia: Plazo o capital invalido para el simulador.{RESET}")

    # Confirmar Transaccion
    print(f"\n{BOLD}¿Desea formalizar y registrar esta inversion en Payflow?{RESET}")
    confirm = input(f"Confirmar inversion real (S/N): ").strip().upper()
    if confirm != 'S':
        print(f"{YELLOW}Operacion cancelada por el usuario.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    exito, folio_o_errs, saldo_act = sistema.realizar_inversion(usuario_actual, es_alto_riesgo, capital, plazo)
    if exito:
        print(f"\n{GREEN}[OK] ¡Inversion autorizada y registrada exitosamente!{RESET}")
        print(f"  {BOLD}Folio de Aprobacion:{RESET} {folio_o_errs}")
        print(f"  {BOLD}Nuevo Saldo Disponible:{RESET} ${saldo_act:,.2f}")
    else:
        print(f"\n{RED}[X] Inversion Rechazada por las reglas de control de riesgos:{RESET}")
        for k, v in folio_o_errs.items():
            print(f"  - {RED}{v}{RESET}")

    input(f"\nPresione Enter para continuar...")

def menu_suscripcion_streaming(sistema, usuario_actual):
    if not usuario_actual:
        print(f"\n{RED}[X] Debe seleccionar un usuario primero.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    limpiar_pantalla()
    imprimir_dashboard(sistema, usuario_actual)
    imprimir_header("SUSCRIPCION STREAMING - MAQUINA DE ESTADOS")

    print(f"\n{BOLD}Diagrama Simplificado de Transiciones:{RESET}")
    print(f"  [INACTIVO]   --- REGISTRO ---> [INACTIVO]")
    print(f"  [INACTIVO]   --- PAGO_EXITOSO ---> [ACTIVO]")
    print(f"  [ACTIVO]     --- PAGO_VENCIDO ---> [MORA]")
    print(f"  [MORA]       --- PAGO_VENCIDO/MORA_AGOTADA ---> [SUSPENDIDO]")
    print(f"  [MORA/SUSP]  --- PAGO_EXITOSO/RECUPERACION ---> [ACTIVO]")
    print(f"  [*]          --- CANCELACION ---> [CANCELADO]")

    print(f"\n{BOLD}Enviar un evento a la suscripcion actual:{RESET}")
    print(f"  {CYAN}[1]{RESET} REGISTRO")
    print(f"  {CYAN}[2]{RESET} PAGO_EXITOSO (Cobra $150.00 de su saldo sin comision)")
    print(f"  {CYAN}[3]{RESET} PAGO_VENCIDO")
    print(f"  {CYAN}[4]{RESET} MORA_AGOTADA")
    print(f"  {CYAN}[5]{RESET} RECUPERACION (Cobra $150.00 de su saldo sin comision)")
    print(f"  {CYAN}[6]{RESET} CANCELACION")
    print(f"  {RED}[R]{RESET} Regresar")

    op = input(f"\n{BOLD}Seleccione el evento a disparar: {RESET}").strip().upper()
    if op == 'R':
        return

    eventos_map = {
        '1': "REGISTRO",
        '2': "PAGO_EXITOSO",
        '3': "PAGO_VENCIDO",
        '4': "MORA_AGOTADA",
        '5': "RECUPERACION",
        '6': "CANCELACION"
    }

    evento = eventos_map.get(op)
    if not evento:
        print(f"{RED}[X] Opcion de evento no valida.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    exito, mensaje, nuevo_estado = sistema.procesar_evento_suscripcion(usuario_actual, evento)
    if exito:
        print(f"\n{GREEN}[OK] Evento '{evento}' procesado con exito.{RESET}")
        print(f"  {mensaje}")
        print(f"  {BOLD}Nuevo Estado de Suscripcion:{RESET} {CYAN}{nuevo_estado}{RESET}")
    else:
        print(f"\n{RED}[X] Evento '{evento}' rechazado:{RESET}")
        print(f"  {mensaje}")

    input(f"\nPresione Enter para continuar...")

def ver_estado_detallado(sistema, usuario_actual):
    if not usuario_actual:
        print(f"\n{RED}[X] Debe seleccionar un usuario primero.{RESET}")
        input(f"\nPresione Enter para continuar...")
        return

    user = sistema.obtener_usuario(usuario_actual)
    if not user:
        return

    limpiar_pantalla()
    imprimir_dashboard(sistema, usuario_actual)
    imprimir_header(f"REPORTE DETALLADO - {usuario_actual.upper()}")

    # Historial de Pagos de Servicios
    print(f"\n{BOLD}{CYAN}--- HISTORIAL DE PAGOS DE SERVICIOS ---{RESET}")
    if not user["pagos"]:
        print("  Ningun pago registrado.")
    else:
        print(f"  {'Concepto':<20} | {'Monto':<12} | {'Comision':<10} | {'Folio de Comprobante'}")
        print(f"  " + "-" * 70)
        for p in user["pagos"]:
            print(f"  {p['concepto']:<20} | ${p['monto']:<11.2f} | ${p['comision']:<9.2f} | {p['folio']}")

    # Historial de Inversiones
    print(f"\n{BOLD}{CYAN}--- HISTORIAL DE INVERSIONES ACTIVAS ---{RESET}")
    if not user["inversiones"]:
        print("  Ninguna inversion registrada.")
    else:
        print(f"  {'Folio':<20} | {'Capital':<12} | {'Plazo':<8} | {'Tipo':<12} | {'Estado'}")
        print(f"  " + "-" * 70)
        for inv in user["inversiones"]:
            tipo = "Alto Riesgo" if inv["es_alto_riesgo"] else "Bajo Riesgo"
            print(f"  {inv['folio']:<20} | ${inv['capital']:<11.2f} | {inv['plazo_meses']:<6}m | {tipo:<12} | {inv['estado']}")

    input(f"\nPresione Enter para regresar al menu...")

def main():
    sistema = SistemaPayflow()
    usuario_actual = None
    
    # Seleccionar primer usuario por defecto si existe alguno
    usuarios = sistema.obtener_usuarios()
    if usuarios:
        usuario_actual = usuarios[0]

    while True:
        limpiar_pantalla()
        imprimir_header("SISTEMA PAYFLOW - MVP INTEGRADO")
        imprimir_dashboard(sistema, usuario_actual)

        print(f"\n{BOLD}MENU PRINCIPAL:{RESET}")
        print(f"  {CYAN}[1]{RESET} Seleccionar / Crear Usuario")
        print(f"  {CYAN}[2]{RESET} Ver Reporte Detallado de Cuenta")
        print(f"  {CYAN}[3]{RESET} Realizar Pago de Servicio (Renta, Luz, Internet)")
        print(f"  {CYAN}[4]{RESET} Simulador y Registro de Inversion")
        print(f"  {CYAN}[5]{RESET} Gestionar Suscripcion de Streaming")
        print(f"  {RED}[6]{RESET} Salir de la Aplicacion")

        opcion = input(f"\n{BOLD}Seleccione una opcion (1-6): {RESET}").strip()

        if opcion == '1':
            limpiar_pantalla()
            nuevo_usuario = menu_usuario(sistema)
            if nuevo_usuario:
                usuario_actual = nuevo_usuario
        elif opcion == '2':
            ver_estado_detallado(sistema, usuario_actual)
        elif opcion == '3':
            menu_pago_servicio(sistema, usuario_actual)
        elif opcion == '4':
            menu_inversiones(sistema, usuario_actual)
        elif opcion == '5':
            menu_suscripcion_streaming(sistema, usuario_actual)
        elif opcion == '6':
            print(f"\n{GREEN}Gracias por utilizar el MVP de Payflow Finance. ¡Hasta pronto!{RESET}\n")
            break
        else:
            print(f"\n{RED}[X] Opcion invalida. Intente de nuevo.{RESET}")
            input(f"\nPresione Enter para continuar...")

if __name__ == '__main__':
    main()
