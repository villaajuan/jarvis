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
        """Inserta una transacción incluyendo la cuenta de origen/destino."""
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
        """Extrae el historial incluyendo la cuenta."""
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
        """Calcula ingresos y gastos, ignorando las transferencias internas a prueba de fallos."""
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
        """Calcula exactamente cuánto dinero hay en CADA cuenta."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
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

    def obtener_estado_pasivos(self) -> dict:
        """Consulta el estado actual de la Tarjeta Nu y sus cupos."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, cupo_total, deuda_actual FROM pasivos")
            resultado = cursor.fetchone()
            conexion.close()
            
            if resultado:
                nombre, cupo_total, deuda_actual = resultado
                cupo_disponible = cupo_total - deuda_actual
                return {
                    "nombre": nombre,
                    "cupo_total": cupo_total,
                    "deuda_actual": deuda_actual,
                    "cupo_disponible": cupo_disponible
                }
            return {}
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al consultar pasivos: {e}")
            return {}

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

    def calcular_deuda_tc(self, mes_filtro: str) -> float:
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT SUM(monto) FROM transacciones 
                WHERE tipo = 'gasto' AND concepto LIKE '%[TC]%' AND fecha LIKE ?
            ''', (f"{mes_filtro}%",))
            resultado = cursor.fetchone()[0]
            conexion.close()
            return resultado if resultado else 0.0
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al calcular deuda TC: {e}")
            return 0.0

    def exportar_csv(self) -> bool:
        """Exporta la base de datos incluyendo la nueva columna de cuenta."""
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