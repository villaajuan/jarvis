from integracion_poo import Transaccion, GestorFinanciero
from datetime import datetime

def mostrar_menu() -> str:
    print("\n--- JARVIS V2.0: MULTICUENTA & PASIVOS ---")
    print("1. Ver transacciones")
    print("2. Registrar nueva transacción")
    print("3. Generar reporte financiero (Multicuenta)")
    print("4. Estado de Tarjeta de Crédito (Nu) & Alertas")
    print("5. Pagar Tarjeta de Crédito (Nu)")
    print("6. Analizar gastos por categoría")
    print("7. Exportar a Excel (CSV)")
    print("8. Salir")
    return input("Selecciona una opción (1-8): ")

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
                    
                ingresos_mes, gastos_mes = gestor.calcular_balance(mes)
                flujo_mes = ingresos_mes - gastos_mes
                
                saldos = gestor.obtener_balances_cuentas()
                # El patrimonio neto real es la suma de todo tu dinero actual
                patrimonio_neto = sum(saldos.values())
                
                print(f"\n--- REPORTE FINANCIERO DE {mes} ---")
                print(f"Ingresos del mes: +${ingresos_mes:,.2f}")
                print(f"Gastos del mes:   -${gastos_mes:,.2f}")
                print(f"Flujo de Caja (Mes): ${flujo_mes:,.2f}")
                print("----------------------------------------")
                print(f"PATRIMONIO NETO TOTAL: ${patrimonio_neto:,.2f}")
                
                print("\n--- DISTRIBUCIÓN POR CUENTAS ---")
                if not saldos:
                    print("No hay datos de cuentas para mostrar.")
                else:
                    for c, saldo in saldos.items():
                        print(f"{c}: ${saldo:,.2f}")
                
                pasivo = gestor.obtener_estado_pasivos_pro()
                if pasivo and pasivo.get('deuda_actual', 0) > 0:
                    print("\n--- ⚠️ ALERTA TÁCTICA DE CRÉDITO ---")
                    print(f"Tienes una deuda activa en {pasivo.get('nombre', 'Tarjeta')} por ${pasivo.get('deuda_actual'):,.2f}.")
                    print("Asegúrate de tener la liquidez separada en tus cuentas operativas para cubrir la cuota.")
                    
            elif opcion == "4":
                print("\n--- ESTADO DE PASIVOS & AUDITORÍA NU ---")
                pasivo = gestor.obtener_estado_pasivos_pro()
                if not pasivo:
                    print("No hay pasivos registrados en el sistema.")
                else:
                    print(f"Tarjeta:         {pasivo.get('nombre')}")
                    print(f"Cupo Total:      ${pasivo.get('cupo_total', 0):,.2f}")
                    print(f"Deuda Actual:    ${pasivo.get('deuda_actual', 0):,.2f}")
                    print(f"Cupo Disponible: ${pasivo.get('cupo_disponible', 0):,.2f}")
                    
                    if pasivo.get('dia_corte'):
                        print(f"Día de Corte:    Día {pasivo['dia_corte']} de cada mes")
                        print(f"Día de Pago:     Día {pasivo['dia_pago']} de cada mes")
                        print(f"----------------------------------------")
                        print(f"[ESTADO]         {pasivo.get('estado_pago')}")
                    
                    if pasivo.get('deuda_actual', 0) > 0:
                        print("\n[ESTADO] Tienes obligaciones diferidas (Ej. Monitor LG a cuotas).")
                    else:
                        print("\n[ESTADO] Tarjeta a paz y salvo. Cupo 100% disponible.")

            elif opcion == "5":
                print("\n--- PAGO DE TARJETA DE CRÉDITO ---")
                pasivo = gestor.obtener_estado_pasivos_pro()
                
                if pasivo and pasivo.get('deuda_actual', 0) > 0:
                    deuda = pasivo['deuda_actual']
                    print(f"Deuda actual de {pasivo['nombre']}: ${deuda:,.2f}")
                    
                    # Cálculo de la cuota milimétrica ajustada a 2 decimales para evitar desfases
                    cuota_sugerida = round(deuda / 6, 2)
                    print(f"Cuota sugerida (1/6 ajustada): ${cuota_sugerida:,.2f}")
                    
                    monto_input = input("Ingresa el monto exacto a pagar (o presiona Enter para la cuota sugerida): ")
                    monto_pago = float(monto_input) if monto_input.strip() else cuota_sugerida
                    
                    cuenta_input = input("¿Desde qué cuenta pagas? (Enter para 'Bancolombia'): ").strip()
                    cuenta_origen = cuenta_input if cuenta_input else "Bancolombia"
                    
                    # Confirmación final de seguridad
                    confirmacion = input(f"¿Confirmas el pago de ${monto_pago:,.2f} descontándolo de {cuenta_origen}? (s/n): ").strip().lower()
                    
                    if confirmacion == 's':
                        if gestor.pagar_pasivo(monto_pago, cuenta_origen):
                            print(f"[OK] Pago procesado exitosamente. Tu deuda ha bajado.")
                        else:
                            print("[ERROR] Fallo al procesar el pago.")
                    else:
                        print("[CANCELADO] El pago no se registró.")
                else:
                    print("No tienes deudas activas para pagar en este momento.")
                    
            elif opcion == "6":
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

            elif opcion == "7":
                print("\nGenerando archivo Excel/CSV...")
                if gestor.exportar_csv():
                    print("[OK] Base de datos exportada con éxito.")
                    print("Revisa la carpeta 'data'. Encontrarás 'reporte_jarvis.csv'.")
                else:
                    print("[ERROR] No se pudo exportar el archivo.")
                    
            elif opcion == "8":
                print("Cerrando Jarvis V2.0. Sistema fuera de línea.")
                break
                
            else:
                print("[ERROR] Opción no válida. Intenta de nuevo.")
                
        except ValueError:
            print("[ERROR] Ingresaste un valor numérico inválido.")
        except Exception as e:
            print(f"[ERROR INESPERADO] {e}")

if __name__ == "__main__":
    main()