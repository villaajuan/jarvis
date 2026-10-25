class Transaccion:
    def __init__(self, concepto: str, monto: float, tipo: str):
        self.concepto = concepto
        self._monto = monto
        self.tipo = tipo

    def obtener_monto(self) -> float:
        return self._monto

    def obtener_resumen(self) -> str:
        simbolo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.tipo.upper()}] {self.concepto}: {simbolo}${self._monto:,.2f}"


# Subclase que hereda de Transaccion
class TransaccionRecurrente(Transaccion):
    def __init__(self, concepto: str, monto: float, tipo: str, frecuencia: str):
        # Invocación al constructor de la clase padre
        super().__init__(concepto, monto, tipo)
        self.frecuencia = frecuencia  # Atributo exclusivo de la subclase

    def obtener_resumen(self) -> str:
        # Sobrescritura del método padre
        resumen_base = super().obtener_resumen()
        return f"{resumen_base} (Frecuencia: {self.frecuencia})"


# Pruebas de ejecución
t_normal = Transaccion("Compra D1", 45000, "gasto")
t_fija = TransaccionRecurrente("Suscripción Internet", 80000, "gasto", "mensual")

print(t_normal.obtener_resumen())
print(t_fija.obtener_resumen())