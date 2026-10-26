from integracion_poo import Transaccion, GestorFinanciero

def mostrar_menu() -> str:
    print("\n--- JARVIS: CONTROL FINANCIERO ---")
    print("1. Ver transacciones")
    print("2. Registrar nueva transacción")
    print("3. Salir")
    return input("Selecciona una opción (1/2/3): ")

def ejecutar_consola():
    # Inicializa la base de datos
    gestor = GestorFinanciero()
    # Carga el historial previo
    transacciones = gestor.cargar_objetos()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            if not transacciones:
                print("\n[INFO] El registro está vacío.")
            else:
                print("\n--- HISTORIAL ---")
                for t in transacciones:
                    print(t.obtener_resumen())

        elif opcion == "2":
            print("\n--- NUEVO REGISTRO ---")
            concepto = input("Concepto (ej. Transporte): ")
            try:
                monto = float(input("Monto (sin puntos ni signos, ej. 15000): "))
                tipo = input("Tipo (ingreso/gasto): ").strip().lower()
                
                if tipo not in ["ingreso", "gasto"]:
                    print("[ERROR] El tipo debe ser 'ingreso' o 'gasto'.")
                    continue

                nueva_t = Transaccion(concepto, monto, tipo)
                transacciones.append(nueva_t)
                gestor.guardar_objetos(transacciones)
                print("[OK] Registro guardado en disco.")
            except ValueError:
                print("[ERROR] El monto debe ser un valor numérico válido.")

        elif opcion == "3":
            print("Cerrando Jarvis. Sistema fuera de línea.")
            break
            
        else:
            print("[ERROR] Comando no reconocido.")

if __name__ == "__main__":
    ejecutar_consola()