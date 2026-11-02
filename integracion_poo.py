import sqlite3
import csv
from datetime import datetime

class Transaccion:
    def __init__(self, concepto: str, monto: float, tipo: str, cuenta: str = "Bancolombia", fecha: str = None):
        self.concepto = concepto
        self._monto = monto
        self.tipo = tipo
        self.cuenta = cuenta
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.fecha}] [{self.cuenta}] [{self.tipo.upper()}] {self.concepto}: {simbolo}${self._monto:,.2f}"

class GestorFinanciero:
    def __init__(self, ruta_bd: str = "data/jarvis.db"):
        self.ruta = ruta_bd

    def registrar_transaccion(self, t: Transaccion) -> bool:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO transacciones (concepto, monto, tipo, cuenta, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (t.concepto, t._monto, t.tipo, t.cuenta, t.fecha))
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al escribir en BD: {e}")
            return False

    def cargar_objetos(self) -> list[Transaccion]:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute("SELECT concepto, monto, tipo, cuenta, fecha FROM transacciones")
            filas = cursor.fetchall()
            conexion.close()
            return [Transaccion(concepto=f[0], monto=f[1], tipo=f[2], cuenta=f[3], fecha=f[4]) for f in filas]
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al leer de BD: {e}")
            return []
    
    def calcular_balance(self, mes_filtro: str) -> tuple[float, float]:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            cursor.execute('''
                SELECT SUM(monto) FROM transacciones 
                WHERE tipo = 'ingreso' AND fecha LIKE ? AND UPPER(concepto) NOT LIKE '%TRANSFERENCIA%'
            ''', (f"{mes_filtro}%",))
            ingresos = cursor.fetchone()[0] or 0.0

            cursor.execute('''
                SELECT SUM(monto) FROM transacciones 
                WHERE tipo = 'gasto' AND fecha LIKE ? AND UPPER(concepto) NOT LIKE '%TRANSFERENCIA%'
            ''', (f"{mes_filtro}%",))
            gastos = cursor.fetchone()[0] or 0.0

            conexion.close()
            return ingresos, gastos
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al calcular en BD: {e}")
            return 0.0, 0.0
        
    def obtener_balances_cuentas(self) -> dict:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            # ¡CORRECCIÓN CRÍTICA! Aquí NO se pueden ignorar las transferencias, 
            # de lo contrario el dinero nunca se mueve a Lulo, Nequi o Efectivo.
            cursor.execute("SELECT cuenta, SUM(monto) FROM transacciones WHERE tipo='ingreso' GROUP BY cuenta")
            ingresos = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor.execute("SELECT cuenta, SUM(monto) FROM transacciones WHERE tipo='gasto' GROUP BY cuenta")
            gastos = {row[0]: row[1] for row in cursor.fetchall()}
            
            conexion.close()
            
            nombres_cuentas = set(list(ingresos.keys()) + list(gastos.keys()))
            saldos = {}
            for c in nombres_cuentas:
                saldos[c] = ingresos.get(c, 0.0) - gastos.get(c, 0.0)
            
            return saldos
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al calcular saldos por cuenta: {e}")
            return {}

    def obtener_estado_pasivos_pro(self) -> dict:
        """Calcula el estado financiero y los días exactos para el pago usando fechas reales."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            # Se intentan traer las columnas de fechas; si la tabla antigua no las tiene, atrapará el error.
            cursor.execute("SELECT nombre, cupo_total, deuda_actual, dia_corte, dia_pago FROM pasivos")
            resultado = cursor.fetchone()
            conexion.close()
            
            if resultado:
                nombre, cupo_total, deuda_actual, dia_corte, dia_pago = resultado
                cupo_disponible = cupo_total - deuda_actual
                
                hoy = datetime.now()
                dia_actual = hoy.day
                
                if dia_actual <= dia_pago:
                    dias_restantes = dia_pago - dia_actual
                    estado_pago = f"Faltan {dias_restantes} días para el pago límite."
                else:
                    estado_pago = "⚠️ Fecha límite de pago vencida este mes. Verifica tu pago."
                
                return {
                    "nombre": nombre,
                    "cupo_total": cupo_total,
                    "deuda_actual": deuda_actual,
                    "cupo_disponible": cupo_disponible,
                    "dia_corte": dia_corte,
                    "dia_pago": dia_pago,
                    "estado_pago": estado_pago
                }
            return {}
        except sqlite3.OperationalError:
            # Fallback en caso de que la tabla de pasivos aún no haya sido migrada con las columnas de fechas
            print("[ADVERTENCIA] La tabla 'pasivos' no tiene las columnas de fechas. Se requiere actualización de BD.")
            return {}
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al consultar pasivos: {e}")
            return {}

    def pagar_pasivo(self, monto_pago: float, cuenta_origen: str = "Bancolombia") -> bool:
        """Registra el pago de la tarjeta descontando de la liquidez y reduciendo la deuda real."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO transacciones (concepto, monto, tipo, cuenta, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', ("[TC] Pago Cuota Nu", monto_pago, "gasto", cuenta_origen, fecha_actual))
            
            cursor.execute('''
                UPDATE pasivos 
                SET deuda_actual = deuda_actual - ? 
                WHERE nombre LIKE '%Nu%'
            ''', (monto_pago,))
            
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al procesar el pago del pasivo: {e}")
            return False

    def analizar_categorias(self, mes_filtro: str, tipo: str = 'gasto') -> list[tuple]:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT SUBSTR(concepto, 1, INSTR(concepto, ']')) AS categoria, 
                       SUM(monto) 
                FROM transacciones 
                WHERE tipo = ? AND fecha LIKE ? AND categoria != ''
                GROUP BY categoria
                ORDER BY SUM(monto) DESC
            ''', (tipo, f"{mes_filtro}%"))
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except sqlite3.Error as e:
            print(f"[ERROR] Falla analítica en BD: {e}")
            return []

    def exportar_csv(self) -> bool:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute("SELECT rowid, concepto, monto, tipo, cuenta, fecha FROM transacciones")
            filas = cursor.fetchall()
            conexion.close()

            with open('data/reporte_jarvis.csv', 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['ID', 'Concepto', 'Monto', 'Tipo', 'Cuenta', 'Fecha'])
                escritor.writerows(filas)
            return True
        except Exception as e:
            print(f"[ERROR] Al exportar a CSV: {e}")
            return False

    def simular_interes_lulo(self, saldo_inicial: float, meses: int, aporte_mensual: float = 0.0, incluir_prima: bool = False, valor_prima: float = 1500000.0) -> list:
        """Proyecta el crecimiento del dinero con interés compuesto al 9.5% E.A., incorporando aportes y primas semestrales."""
        tasa_ea = 0.095
        tasa_mensual = (1 + tasa_ea)**(1/12) - 1
        
        proyeccion = []
        saldo_actual = saldo_inicial
        
        for mes in range(1, meses + 1):
            interes_ganado = saldo_actual * tasa_mensual
            
            # Sumar aporte mensual y la prima si el mes es múltiplo de 6 (junio, diciembre...)
            aporte_total_mes = aporte_mensual
            if incluir_prima and (mes % 6 == 0):
                aporte_total_mes += valor_prima
                
            saldo_actual += interes_ganado + aporte_total_mes
            
            proyeccion.append({
                "mes": mes,
                "interes_ganado": interes_ganado,
                "aporte": aporte_total_mes,
                "saldo_final": saldo_actual
            })
            
        return proyeccion