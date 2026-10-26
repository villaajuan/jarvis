import json
from pathlib import Path


class Transaccion:

    def __init__(self, concepto: str, monto: float, tipo: str):
        self.concepto = concepto
        self._monto = monto
        self.tipo = tipo

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.tipo.upper()}] {self.concepto}: {simbolo}${self._monto:,.2f}"

    def to_dict(self) -> dict:
        """Convierte la instancia en un diccionario para guardar en JSON."""
        return {
            "concepto": self.concepto,
            "monto": self._monto,
            "tipo": self.tipo,
        }

    @classmethod
    def from_dict(cls, datos: dict):
        """Crea una instancia de Transaccion a partir de un diccionario."""
        return cls(
            concepto=datos["concepto"],
            monto=datos["monto"],
            tipo=datos["tipo"],
        )


class GestorFinanciero:

    def __init__(self, ruta_archivo: str = "data/transacciones_objetos.json"):
        self.ruta = Path(ruta_archivo)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def guardar_objetos(self, lista_objetos: list[Transaccion]) -> bool:
        """Serializa una lista de objetos Transaccion y los guarda en JSON."""
        try:
            # Convierte cada objeto a diccionario usando to_dict()
            datos_dict = [obj.to_dict() for obj in lista_objetos]
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(datos_dict, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[ERROR] Error de escritura: {e}")
            return False

    def cargar_objetos(self) -> list[Transaccion]:
        """Lee el JSON y reconstruye la lista como instancias de Transaccion."""
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                datos_dict = json.load(f)
                # Convierte cada diccionario a objeto usando from_dict()
                return [Transaccion.from_dict(d) for d in datos_dict]
        except (FileNotFoundError, json.JSONDecodeError):
            return []


# Prueba de integración
if __name__ == "__main__":
    gestor = GestorFinanciero()

    # 1. Crear objetos en memoria
    t1 = Transaccion("Nequi Pago Servicios", 65000.0, "gasto")
    t2 = Transaccion("Honorarios Freelance", 350000.0, "ingreso")

    # 2. Guardar lista de objetos
    gestor.guardar_objetos([t1, t2])
    print("[OK] Objetos guardados exitosamente en JSON.")

    # 3. Cargar desde disco y verificar comportamiento de objeto
    objetos_recuperados = gestor.cargar_objetos()
    print(f"\nSe cargaron {len(objetos_recuperados)} objetos desde el archivo:")

    for obj in objetos_recuperados:
        # Demostración: ejecutan métodos de la clase Transaccion
        print(" ->", obj.obtener_resumen())