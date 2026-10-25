class Transaccion:
    def __init__(self, concepto: str, monto: float, tipo: str):
        self.concepto = concepto
        self._monto = monto  # Atributo protegido (encapsulado)
        self.tipo = tipo

    def obtener_monto(self) -> float:
        return self._monto

    def aplicar_descuento(self, porcentaje: float):
        descuento = self._monto * (porcentaje / 100)
        self._monto -= descuento

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.tipo.upper()}] {self.concepto}: {simbolo}${self._monto:,.2f}"


# Prueba de la clase encapsulada
t1 = Transaccion("Pago tarjeta nu", 120000, "gasto")
t1.aplicar_descuento(10)

print(f"Monto procesado: ${t1.obtener_monto():,.2f}")
print(t1.obtener_resumen())