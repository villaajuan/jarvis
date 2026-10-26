import json
from pathlib import Path


class GestorFinanciero:

    def __init__(self, ruta_archivo: str = "data/transacciones.json"):
        self.ruta = Path(ruta_archivo)
        # Asegurar que el directorio data/ exista
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def guardar_transacciones(self, lista_datos: list) -> bool:
        """Guarda una lista de diccionarios en el archivo JSON."""
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(lista_datos, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[ERROR] No se pudo escribir en el archivo: {e}")
            return False

    def cargar_transacciones(self) -> list:
        """Carga y retorna los datos del archivo JSON. Si falla, retorna una lista vacía."""
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(
                "[WARN] Archivo no encontrado. Se creará uno nuevo al guardar."
            )
            return []
        except json.JSONDecodeError:
            print(
                "[ERROR] El archivo está corrupto. Retornando estructura limpia."
            )
            return []


# Prueba del gestor
if __name__ == "__main__":
    gestor = GestorFinanciero()

    # 1. Intentar cargar datos existentes
    datos = gestor.cargar_transacciones()
    print(f"Datos cargados iniciales: {datos}")

    # 2. Agregar un registro de prueba
    nueva_transaccion = {
        "concepto": "Compra herramientas",
        "monto": 85000.0,
        "tipo": "gasto",
    }
    datos.append(nueva_transaccion)

    # 3. Guardar en disco
    if gestor.guardar_transacciones(datos):
        print("[OK] Persistencia exitosa en data/transacciones.json")