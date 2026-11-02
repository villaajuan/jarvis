from integracion_poo import Transaccion, GestorFinanciero
from datetime import datetime

def mostrar_menu() -> str:
    print("\n--- JARVIS V2.0: MULTICUENTA & PASIVOS ---")
    print("1. Ver transacciones")
    print("2. Registrar nueva transacción")
    print("3. Generar reporte financiero (Multicuenta)")
    print("4. Estado de Tarjeta de Crédito (Nu)")
    print("5. Analizar gastos por categoría")
    print("6. Exportar a Excel (CSV)")
    print("7. Salir")
    return input("Selecciona una opción (1-7): ")

def main():
    gestor = GestorFinanciero()
    print("Iniciando sistema Jarvis V2.0...")
    
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
                
                print("\nCuentas: Bancolombia, Lulo Bank, Efectivo, Nequi, Bolsillos")
                cuenta_input = input("Cuenta (Enter para 'Bancolombia'): ").strip()
                cuenta = cuenta_input if cuenta_input else "Bancolombia"
                
                fecha_input = input("Fecha (YYYY-MM-DD HH:MM:SS) o Enter para hoy: ").strip()
                fecha = fecha_input if fecha_input else None
                
                nueva_t = Transaccion(concepto, monto, tipo, cuenta, fecha)
                
                if gestor.registrar_transaccion(nueva_t):
                    print(f"[OK] Transacción guardada exitosamente en {cuenta}.")
                    
            elif opcion == "3":
                mes = input("\nIngresa el mes a consultar (Enter para actual YYYY-MM): ")
                if not mes.strip():
                    mes = datetime.now().strftime("%Y-%m")
                    
                ingresos, gastos = gestor.calcular_balance(mes)
                balance_total = ingresos - gastos
                
                print(f"\n--- REPORTE FINANCIERO DE {mes} ---")
                print(f"Total Ingresos: +${ingresos:,.2f}")
                print(f"Total Gastos:   -${gastos:,.2f}")
                print(f"PATRIMONIO NETO: ${balance_total:,.2f}")
                
                print("\n--- DISTRIBUCIÓN POR CUENTAS ---")
                saldos = gestor.obtener_balances_cuentas()
                if not saldos:
                    print("No hay datos de cuentas para mostrar.")
                else:
                    for c, saldo in saldos.items():
                        print(f"{c}: ${saldo:,.2f}")
                
                deuda_tc = gestor.calcular_deuda_tc(mes)
                if deuda_tc > 0:
                    print("\n--- ALERTA TÁCTICA DE CRÉDITO ---")
                    print(f"Deuda mensual detectada [TC]: ${deuda_tc:,.2f}")
                    print("(Este dinero ya se descontó de tu Patrimonio. Mantenlo líquido para pagar a Nu).")

            elif opcion == "4":
                # NUEVO MÓDULO DE PASIVOS
                print("\n--- ESTADO DE PASIVOS Y LÍNEA DE CRÉDITO ---")
                pasivo = gestor.obtener_estado_pasivos()
                if not pasivo:
                    print("No hay pasivos registrados en el sistema.")
                else:
                    print(f"Tarjeta: {pasivo['nombre']}")
                    print(f"Cupo Total:      ${pasivo['cupo_total']:,.2f}")
                    print(f"Deuda Actual:    ${pasivo['deuda_actual']:,.2f}")
                    print(f"Cupo Disponible: ${pasivo['cupo_disponible']:,.2f}")
                    
            elif opcion == "5":
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

            elif opcion == "6":
                print("\nGenerando archivo Excel/CSV...")
                if gestor.exportar_csv():
                    print("[OK] Base de datos exportada con éxito.")
                    print("Revisa la carpeta 'data'. Encontrarás 'reporte_jarvis.csv'.")
                else:
                    print("[ERROR] No se pudo exportar el archivo.")
                    
            elif opcion == "7":
                print("Cerrando Jarvis V2.0. Sistema fuera de línea.")
                break
                
            else:
                print("[ERROR] Opción no válida. Intenta de nuevo.")
                
        except ValueError:
            print("[ERROR] Ingresaste un valor inválido (asegúrate de no usar letras o signos en el monto).")
        except Exception as e:
            print(f"[ERROR INESPERADO] {e}")

if __name__ == "__main__":
    main()