from integracion_poo import Transaccion, GestorFinanciero
from datetime import datetime

def mostrar_menu() -> str:
    print("\n--- JARVIS: CONTROL FINANCIERO (SQLITE) ---")
    print("1. Ver transacciones")
    print("2. Registrar nueva transacción")
    print("3. Generar reporte mensual")
    print("4. Analizar gastos por categoría")
    print("5. Exportar a Excel (CSV)")
    print("6. Salir")
    return input("Selecciona una opción (1/2/3/4/5/6): ")

def main():
    gestor = GestorFinanciero()
    print("Iniciando sistema Jarvis...")
    
    while True:
        try:
            opcion = mostrar_menu()
            
            if opcion == "1":
                transacciones = gestor.cargar_objetos()
                print("\n--- HISTORIAL DE TRANSACCIONES ---")
                if not transacciones:
                    print("No hay transacciones registradas.")
                else:
                    for t in transacciones:
                        print(t.obtener_resumen())
                        
            elif opcion == "2":
                print("\n--- REGISTRAR TRANSACCIÓN ---")
                concepto = input("Concepto (ej. [Salario] Quincena): ")
                monto = float(input("Monto (sin puntos ni comas): "))
                tipo = input("Tipo (ingreso/gasto): ").lower()
                fecha_input = input("Fecha (YYYY-MM-DD HH:MM:SS) o Enter para hoy: ")
                
                fecha = fecha_input if fecha_input.strip() else None
                nueva_t = Transaccion(concepto, monto, tipo, fecha)
                
                if gestor.registrar_transaccion(nueva_t):
                    print("[OK] Transacción guardada en la base de datos.")
                    
            elif opcion == "3":
                mes = input("\nIngresa el mes a consultar (Enter para actual YYYY-MM): ")
                if not mes.strip():
                    mes = datetime.now().strftime("%Y-%m")
                    
                ingresos, gastos = gestor.calcular_balance(mes)
                balance = ingresos - gastos
                
                print(f"\n--- REPORTE FINANCIERO DE {mes} ---")
                print(f"Total Ingresos: +${ingresos:,.2f}")
                print(f"Total Gastos:   -${gastos:,.2f}")
                print(f"BALANCE NETO:   ${balance:,.2f}")
                
                # Alerta táctica de deuda
                deuda_tc = gestor.calcular_deuda_tc(mes)
                if deuda_tc > 0:
                    print("\n--- ALERTA TÁCTICA DE CRÉDITO ---")
                    print(f"Deuda acumulada en Nu [TC]: ${deuda_tc:,.2f}")
                    print("(Jarvis ya descontó este dinero de tu Balance Neto. Guárdalo para la cuota).")
                    
            elif opcion == "4":
                mes = input("\nIngresa el mes a consultar (Enter para actual YYYY-MM): ")
                if not mes.strip():
                    mes = datetime.now().strftime("%Y-%m")
                    
                print(f"\n--- ANÁLISIS DE GASTOS POR CATEGORÍA ({mes}) ---")
                resultados = gestor.analizar_categorias(mes, 'gasto')
                
                if not resultados:
                    print("No hay gastos registrados en este mes.")
                else:
                    for categoria, total in resultados:
                        print(f"{categoria}: ${total:,.2f}")

            elif opcion == "5":
                print("\nGenerando archivo Excel/CSV...")
                if gestor.exportar_csv():
                    print("[OK] Base de datos exportada con éxito.")
                    print("Revisa la carpeta 'data'. Encontrarás 'reporte_jarvis.csv'.")
                else:
                    print("[ERROR] No se pudo exportar el archivo.")
                    
            elif opcion == "6":
                print("Cerrando Jarvis. Sistema fuera de línea.")
                break
                
            else:
                print("[ERROR] Opción no válida. Intenta de nuevo.")
                
        except ValueError:
            print("[ERROR] Ingresaste un valor inválido (asegúrate de no usar letras o signos en el monto).")
        except Exception as e:
            print(f"[ERROR INESPERADO] {e}")

if __name__ == "__main__":
    main()