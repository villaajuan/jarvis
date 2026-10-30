from integracion_poo import Transaccion, GestorFinanciero
from datetime import datetime

def mostrar_menu() -> str:
    print("\n--- JARVIS: CONTROL FINANCIERO (SQLITE) ---")
    print("1. Ver transacciones")
    print("2. Registrar nueva transacción")
    print("3. Generar reporte mensual")
    print("4. Analizar gastos por categoría")
    print("5. Salir")
    return input("Selecciona una opción (1/2/3/4/5): ")

def ejecutar_consola():
    gestor = GestorFinanciero()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            transacciones = gestor.cargar_objetos()
            if not transacciones:
                print("\n[INFO] El registro está vacío.")
            else:
                print("\n--- HISTORIAL ---")
                for t in transacciones:
                    print(t.obtener_resumen())

        elif opcion == "2":
            print("\n--- NUEVO REGISTRO ---")
            concepto = input("Concepto (ej. [Mercado] D1): ")
            try:
                monto = float(input("Monto (sin puntos ni signos, ej. 15000): "))
                tipo = input("Tipo (ingreso/gasto): ").strip().lower()
                
                if tipo not in ["ingreso", "gasto"]:
                    print("[ERROR] El tipo debe ser 'ingreso' o 'gasto'.")
                    continue

                # NUEVO: Lógica para manejar fechas en el pasado
                fecha_input = input("Fecha (YYYY-MM-DD) [Presiona Enter para hoy]: ").strip()
                
                if fecha_input:
                    # Si el usuario escribe una fecha, le concatenamos la hora actual para mantener el formato SQL
                    hora_actual = datetime.now().strftime("%H:%M:%S")
                    fecha_final = f"{fecha_input} {hora_actual}"
                else:
                    # Si da Enter, enviamos None y la clase Transaccion pone la fecha y hora exacta
                    fecha_final = None

                # --- NUEVA REGLA DE NEGOCIO: FACTOR ESFUERZO ---
                if "[Ocio]" in concepto and tipo == "gasto" and monto >= 50000:
                    print("\n[ALERTA JARVIS - FACTOR ESFUERZO]")
                    print(f"⚠️  Atención: ${monto:,.2f} equivalen a un turno pesado de descargue en la planta.")
                    confirmacion = input("¿Estás seguro de que deseas intercambiar esa energía física por este gasto? (s/n): ").strip().lower()
                    
                    if confirmacion != 's':
                        print("[INFO] Transacción abortada. Excelente decisión, capital protegido.")
                        continue  # Aborta y vuelve al menú principal

                # Si no es de ocio, si es menor a 40k, o si el usuario dijo 's', procedemos a guardar:
                nueva_t = Transaccion(concepto, monto, tipo, fecha=fecha_final)
                
                if gestor.registrar_transaccion(nueva_t):
                    print("[OK] Registro insertado exitosamente en SQLite.")
                    
            except ValueError:
                print("[ERROR] El monto debe ser un valor numérico válido.")

        elif opcion == "3":
            mes_actual = datetime.now().strftime("%Y-%m")
            mes_filtro = input(f"Ingresa el mes a consultar (Enter para {mes_actual}): ")
            
            if not mes_filtro:
                mes_filtro = mes_actual
            
            ingresos, gastos = gestor.calcular_balance(mes_filtro)
            balance = ingresos - gastos
            deuda_tc = gestor.calcular_deuda_tc(mes_filtro)
            
            print(f"\n--- REPORTE FINANCIERO DE {mes_filtro} ---")
            print(f"Total Ingresos: +${ingresos:,.2f}")
            print(f"Total Gastos:   -${gastos:,.2f}")
            print(f"BALANCE NETO:   ${balance:,.2f}")
            
            # --- NUEVA REGLA: GESTIÓN TÁCTICA NU ---
            if deuda_tc > 0:
                print(f"\n--- ALERTA TÁCTICA DE CRÉDITO ---")
                print(f"Deuda acumulada en Nu [TC]: ${deuda_tc:,.2f}")
                print(f"(Jarvis ya descontó este dinero de tu Balance Neto. Guárdalo para la cuota).")
        
        elif opcion == "4":
            mes_actual = datetime.now().strftime("%Y-%m")
            mes_filtro = input(f"Ingresa el mes a consultar (Enter para {mes_actual}): ")
            
            if not mes_filtro:
                mes_filtro = mes_actual
                
            print(f"\n--- ANÁLISIS DE GASTOS: {mes_filtro} ---")
            categorias = gestor.analizar_categorias(mes_filtro, 'gasto')
            
            if not categorias:
                print("No hay gastos registrados para analizar en este mes.")
            else:
                for cat, total in categorias:
                    print(f"{cat:<15}: ${total:,.2f}")

        elif opcion == "5":
            print("Cerrando Jarvis. Sistema fuera de línea.")
            break
            
        else:
            print("[ERROR] Comando no reconocido.")

if __name__ == "__main__":
    ejecutar_consola()