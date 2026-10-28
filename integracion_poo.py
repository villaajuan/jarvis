import sqlite3
from datetime import datetime

class Transaccion:
    def __init__(self, concepto: str, monto: float, tipo: str, fecha: str = None):
        self.concepto = concepto
        self._monto = monto
        self.tipo = tipo
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.fecha}] [{self.tipo.upper()}] {self.concepto}: {simbolo}${self._monto:,.2f}"

class GestorFinanciero:
    def __init__(self, ruta_bd: str = "data/jarvis.db"):
        self.ruta = ruta_bd

    def registrar_transaccion(self, t: Transaccion) -> bool:
        """Inserta una única transacción en la base de datos relacional."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO transacciones (concepto, monto, tipo, fecha)
                VALUES (?, ?, ?, ?)
            ''', (t.concepto, t._monto, t.tipo, t.fecha))
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al escribir en BD: {e}")
            return False

    def cargar_objetos(self) -> list[Transaccion]:
        """Ejecuta un SELECT y convierte las filas de SQL en objetos Python."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute("SELECT concepto, monto, tipo, fecha FROM transacciones")
            filas = cursor.fetchall()
            conexion.close()
            
            # Convierte las tuplas devueltas por SQL en instancias de la clase
            return [Transaccion(concepto=f[0], monto=f[1], tipo=f[2], fecha=f[3]) for f in filas]
        
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al leer de BD: {e}")
            return []
    
    def calcular_balance(self, mes_filtro: str) -> tuple[float, float]:
        """Delega el cálculo matemático (sumas) al motor de la base de datos."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            # 1. Suma todos los ingresos del mes directamente en SQL
            cursor.execute('''
                SELECT SUM(monto) FROM transacciones 
                WHERE tipo = 'ingreso' AND fecha LIKE ?
            ''', (f"{mes_filtro}%",))
            
            # fetchone() trae el primer registro. [0] extrae el número. 'or 0.0' evita errores si no hay datos.
            ingresos = cursor.fetchone()[0] or 0.0

            # 2. Suma todos los gastos del mes
            cursor.execute('''
                SELECT SUM(monto) FROM transacciones 
                WHERE tipo = 'gasto' AND fecha LIKE ?
            ''', (f"{mes_filtro}%",))
            
            gastos = cursor.fetchone()[0] or 0.0

            conexion.close()
            return ingresos, gastos
            
        except sqlite3.Error as e:
            print(f"[ERROR] Falla al calcular en BD: {e}")
            return 0.0, 0.0