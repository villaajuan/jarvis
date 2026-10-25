class Transaccion:
    def __init__(self, concepto: str, monto: float, tipo: str):
        self.concepto = concepto
        self.monto = monto
        self.tipo = tipo  # "ingreso" o "gasto"

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.tipo.upper()}] {self.concepto}: {simbolo}${self.monto:,.2f}"

    def aplicar_descuento(self, porcentaje: float):
        descuento = self.monto * (porcentaje / 100)
        self.monto -= descuento


# Creación de objetos (instancias)
t1 = Transaccion("Pago tarjeta nu", 120000, "gasto")
t2 = Transaccion("Abono lulo bank", 450000, "ingreso")

# Aplicación del reto: descuento del 10% sobre el gasto t1
t1.aplicar_descuento(10)

# Ejecución de métodos
print(t1.obtener_resumen())
print(t2.obtener_resumen())
