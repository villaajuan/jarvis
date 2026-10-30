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

    def analizar_categorias(self, mes_filtro: str, tipo: str = 'gasto') -> list[tuple]:
        """Agrupa y suma los montos por categoría extrayendo los corchetes en SQL."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            # INSTR busca el corchete de cierre ']'. 
            # SUBSTR recorta el texto desde el inicio hasta ese corchete.
            # GROUP BY fusiona las categorías idénticas y SUM() suma la plata.
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
        """Suma los gastos hechos con Tarjeta de Crédito para separar el pago."""
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            
            # Sumamos todos los gastos que tengan [TC] en su concepto
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