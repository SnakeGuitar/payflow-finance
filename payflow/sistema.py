import json
import os
from .inversiones import Payflow as InversionPayflow
from .validador import ValidadorInversión
from .suscripcion_streaming import SuscripcionStreaming
from .transaccion import Pago as PagoService, CuentaUsuario

DB_FILE = "payflow_db.json"

DEFAULT_DB = {
    "Alice": {
        "id": "Alice",
        "saldo_disponible": 15000.0,
        "cuenta_nueva": False,
        "suscripcion_estado": "ACTIVO",
        "inversiones": [],
        "pagos": []
    },
    "Bob": {
        "id": "Bob",
        "saldo_disponible": 1200.0,
        "cuenta_nueva": True,
        "suscripcion_estado": "INACTIVO",
        "inversiones": [],
        "pagos": []
    },
    "Charlie": {
        "id": "Charlie",
        "saldo_disponible": 500.0,
        "cuenta_nueva": False,
        "suscripcion_estado": "MORA",
        "inversiones": [],
        "pagos": []
    }
}

class SistemaPayflow:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.db = {}
        self.load_db()

    def load_db(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.db = json.load(f)
            except Exception:
                self.db = DEFAULT_DB.copy()
                self.save_db()
        else:
            self.db = DEFAULT_DB.copy()
            self.save_db()

    def save_db(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4, ensure_ascii=False)

    def obtener_usuarios(self):
        return list(self.db.keys())

    def obtener_usuario(self, user_id):
        return self.db.get(user_id)

    def crear_usuario(self, user_id, saldo_inicial, cuenta_nueva, edad=18, tiene_id=True):
        if user_id in self.db:
            return False, f"El usuario '{user_id}' ya existe."
        if saldo_inicial < 0:
            return False, "El saldo inicial no puede ser negativo."
        
        from .acceso_seguridad import validar_registro
        if validar_registro(edad, tiene_id) == "ACCESO_DENEGADO":
            return False, "ACCESO_DENEGADO: Registro rechazado por edad o identificacion invalida."
        
        self.db[user_id] = {
            "id": user_id,
            "saldo_disponible": float(saldo_inicial),
            "cuenta_nueva": bool(cuenta_nueva),
            "suscripcion_estado": "INACTIVO",
            "inversiones": [],
            "pagos": []
        }
        self.save_db()
        return True, None

    def realizar_pago_servicio(self, user_id, monto, concepto):
        user = self.obtener_usuario(user_id)
        if not user:
            return False, "Usuario no encontrado.", None

        cuenta = CuentaUsuario(user_id, user["saldo_disponible"])
        es_fallido, comprobante = PagoService.realizar_pago(monto, cuenta, concepto)

        if es_fallido:
            from .transaccion import PagoCapaSuperior
            if not PagoCapaSuperior.es_concepto_valido(concepto):
                err = f"Concepto de pago '{concepto}' no es valido."
            else:
                costo_total = monto + (0.0 if concepto == "INTERNET" else 15.0)
                err = f"Saldo insuficiente. Costo total: ${costo_total:.2f}, Saldo disponible: ${user['saldo_disponible']:.2f}"
            return False, err, user["saldo_disponible"]

        user["saldo_disponible"] = cuenta.saldo_disponible
        user["pagos"].append({
            "folio": comprobante,
            "concepto": concepto,
            "monto": monto,
            "comision": 0.0 if concepto == "INTERNET" else 15.0
        })
        self.save_db()
        return True, comprobante, user["saldo_disponible"]

    def validar_inversion(self, monto, plazo_meses, perfil):
        return ValidadorInversión.validar_inversión(monto, plazo_meses, perfil)

    def realizar_inversion(self, user_id, es_alto_riesgo, capital, plazo_meses):
        user = self.obtener_usuario(user_id)
        if not user:
            return False, "Usuario no encontrado.", None

        inversion_engine = InversionPayflow(user["saldo_disponible"], user["cuenta_nueva"])
        folio, errores = inversion_engine.realizar_inversion(es_alto_riesgo, capital, plazo_meses)

        if errores:
            errores_filtrados = {k: v for k, v in errores.items() if v is not None}
            return False, errores_filtrados, user["saldo_disponible"]

        user["saldo_disponible"] -= capital
        user["inversiones"].append({
            "folio": folio,
            "capital": capital,
            "plazo_meses": plazo_meses,
            "es_alto_riesgo": es_alto_riesgo,
            "estado": inversion_engine.estado
        })
        self.save_db()
        return True, folio, user["saldo_disponible"]

    def procesar_evento_suscripcion(self, user_id, evento):
        user = self.obtener_usuario(user_id)
        if not user:
            return False, "Usuario no encontrado.", None

        estado_actual = user["suscripcion_estado"]
        
        if not SuscripcionStreaming.es_transicion_valida(estado_actual, evento):
            return False, f"Transicion invalida: no se puede aplicar {evento} en estado {estado_actual}.", estado_actual

        if evento in ["PAGO_EXITOSO", "RECUPERACION"]:
            costo_suscripcion = 150.0
            cuenta = CuentaUsuario(user_id, user["saldo_disponible"])
            es_fallido, comprobante = PagoService.realizar_pago(costo_suscripcion, cuenta, "INTERNET")
            if es_fallido:
                return False, f"Pago de suscripcion fallido por saldo insuficiente (${costo_suscripcion:.2f} necesarios).", estado_actual
            
            user["saldo_disponible"] = cuenta.saldo_disponible
            user["pagos"].append({
                "folio": comprobante,
                "concepto": "INTERNET (STREAMING)",
                "monto": costo_suscripcion,
                "comision": 0.0
            })

        nuevo_estado = self.obtener_siguiente_estado(estado_actual, evento)
        user["suscripcion_estado"] = nuevo_estado
        self.save_db()
        return True, f"Suscripcion actualizada exitosamente a {nuevo_estado}.", nuevo_estado

    def obtener_siguiente_estado(self, estado_actual, evento):
        if evento == "REGISTRO":
            return "INACTIVO"
        if evento in ["PAGO_EXITOSO", "RECUPERACION"]:
            return "ACTIVO"
        if evento == "CANCELACION":
            return "CANCELADO"
        if evento == "PAGO_VENCIDO":
            if estado_actual == "ACTIVO":
                return "MORA"
            if estado_actual in ["MORA", "SUSPENDIDO"]:
                return "SUSPENDIDO"
        if evento == "MORA_AGOTADA":
            return "SUSPENDIDO"
        return estado_actual

    def realizar_transferencia(self, user_id, monto, hora, tipo_cuenta, token_activo=False):
        user = self.obtener_usuario(user_id)
        if not user:
            return False, "Usuario no encontrado.", None

        from .transferencia import Transferencia as TransferEngine
        transfer_engine = TransferEngine(user["saldo_disponible"])
        exito, msg = transfer_engine.procesar_transferencia(monto, hora, tipo_cuenta, token_activo)

        if not exito:
            return False, msg, user["saldo_disponible"]

        user["saldo_disponible"] = transfer_engine.saldo_disponible
        if "transferencias" not in user:
            user["transferencias"] = []
        
        user["transferencias"].append({
            "monto": monto,
            "hora": hora,
            "tipo_cuenta": tipo_cuenta,
            "estado": transfer_engine.estado
        })
        self.save_db()
        return True, msg, user["saldo_disponible"]
