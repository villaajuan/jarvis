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
    print("8. Simulador Interés Compuesto (Lulo Bank)")
    print("9. Simulador de Compras a Cuotas (Tarjeta Nu)")
    print("10. Salir")
    return input("Selecciona una opción (1-10): ")

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
                    
                    cuota_sugerida = round(deuda / 6, 2)
                    print(f"Cuota sugerida (1/6 ajustada): ${cuota_sugerida:,.2f}")
                    
                    monto_input = input("Ingresa el monto exacto a pagar (o presiona Enter para la cuota sugerida): ")
                    monto_pago = float(monto_input) if monto_input.strip() else cuota_sugerida
                    
                    cuenta_input = input("¿Desde qué cuenta pagas? (Enter para 'Bancolombia'): ").strip()
                    cuenta_origen = cuenta_input if cuenta_input else "Bancolombia"
                    
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
                
                tipo_input = input("¿Qué deseas analizar? (1: Gastos, 2: Ingresos) [Enter para Gastos]: ").strip()
                tipo_analisis = 'ingreso' if tipo_input == '2' else 'gasto'
                etiqueta = "INGRESOS" if tipo_analisis == 'ingreso' else "GASTOS"
                    
                print(f"\n--- ANÁLISIS VISUAL DE {etiqueta} ({mes}) ---")
                
                resultados = gestor.analizar_categorias(mes, tipo_analisis)
                
                if not resultados:
                    print(f"No hay {etiqueta.lower()} registrados en este mes.")
                else:
                    max_monto = max([total for _, total in resultados])
                    suma_total = sum([total for _, total in resultados])
                    ancho_maximo_barra = 40  
                    
                    for categoria, total in resultados:
                        if max_monto > 0:
                            longitud_barra = int((total / max_monto) * ancho_maximo_barra)
                        else:
                            longitud_barra = 0
                            
                        porcentaje = (total / suma_total) * 100 if suma_total > 0 else 0
                        barra = "█" * longitud_barra
                        
                        print(f"{categoria:<15} | {barra} ${total:,.2f} ({porcentaje:.1f}%)")

            elif opcion == "7":
                print("\nGenerando archivo Excel/CSV...")
                if gestor.exportar_csv():
                    print("[OK] Base de datos exportada con éxito.")
                    print("Revisa la carpeta 'data'. Encontrarás 'reporte_jarvis.csv'.")
                else:
                    print("[ERROR] No se pudo exportar el archivo.")
                    
            elif opcion == "8":
                print("\n--- SIMULADOR DE INTERÉS COMPUESTO (LULO BANK - 9.5% E.A.) ---")
                saldos = gestor.obtener_balances_cuentas()
                saldo_lulo = saldos.get("Lulo Bank", 0.0)
                
                print(f"Saldo base detectado en Lulo Bank: ${saldo_lulo:,.2f}")
                
                try:
                    meses = int(input("¿Cuántos meses deseas proyectar? (Ej. 12, 24, 36): "))
                    aporte = input("¿Harás un aporte mensual extra? (Ingresa el monto o Enter para $0): ")
                    aporte_mensual = float(aporte) if aporte.strip() else 0.0
                    
                    prima_input = input("¿Deseas simular la inyección de tu prima semestral (~$1,500,000 en meses 6, 12, 18...)? (s/n): ").strip().lower()
                    incluir_prima = True if prima_input == 's' else False
                    
                    proyeccion = gestor.simular_interes_lulo(saldo_lulo, meses, aporte_mensual, incluir_prima)
                    
                    print(f"\n--- RESULTADOS A {meses} MESES ---")
                    print(f"{'Mes':<5} | {'Aporte Total Mes':<16} | {'Interés Mes':<15} | {'Saldo Acumulado'}")
                    print("-" * 65)
                    
                    total_interes = 0
                    total_aportado = 0
                    for p in proyeccion:
                        total_interes += p['interes_ganado']
                        total_aportado += p['aporte']
                        if meses <= 24 or p['mes'] % 6 == 0 or p['mes'] == meses:
                            print(f"{p['mes']:<5} | ${p['aporte']:<15,.2f} | ${p['interes_ganado']:<14,.2f} | ${p['saldo_final']:,.2f}")
                            
                    print("-" * 65)
                    print(f"Capital base inicial: ${saldo_lulo:,.2f}")
                    print(f"Total capital inyectado (Aportes + Primas): ${total_aportado:,.2f}")
                    print(f"Total Intereses Pasivos Ganados: ${total_interes:,.2f}")
                    print(f"GRAN TOTAL PROYECTADO: ${proyeccion[-1]['saldo_final']:,.2f}")
                    
                except ValueError:
                    print("[ERROR] Ingresaste un valor numérico inválido.")
                except AttributeError:
                    print("[ERROR] Falta guardar la función en integracion_poo.py")
                    
            elif opcion == "9":
                print("\n--- SIMULADOR DE COMPRAS A CUOTAS (TARJETA NU) ---")
                pasivo = gestor.obtener_estado_pasivos_pro()
                
                if not pasivo:
                    print("[ERROR] No se detectó ninguna tarjeta configurada.")
                else:
                    cupo_disp = pasivo.get('cupo_disponible', 0)
                    print(f"Cupo disponible en {pasivo.get('nombre', 'Nu')}: ${cupo_disp:,.2f}")
                    
                    try:
                        valor_compra = float(input("Ingresa el valor de la compra que deseas simular (sin puntos): "))
                        
                        if valor_compra > cupo_disp:
                            print(f"\n[ALERTA ROJA] La compra (${valor_compra:,.2f}) supera tu cupo disponible (${cupo_disp:,.2f}).")
                            print("Sugerencia: Paga tu cuota de este mes o realiza un abono a capital antes de comprar.")
                        else:
                            print(f"\n[APROBADO] Tienes cupo suficiente para esta compra.")
                            cuotas = input("¿A cuántas cuotas deseas diferirlo? (Ej. 1, 3, 6, 12): ")
                            num_cuotas = int(cuotas) if cuotas.strip() else 1
                            
                            # Asumimos 0% interés de Nu en compras diferidas estándar para el simulador base
                            cuota_mensual = valor_compra / num_cuotas
                            print(f"\n--- PROYECCIÓN DE PAGO (0% Interés asumido) ---")
                            print(f"Valor Total: ${valor_compra:,.2f}")
                            print(f"Número de cuotas: {num_cuotas}")
                            print(f"Valor de cada cuota: ${cuota_mensual:,.2f} al mes")
                            print(f"Nuevo cupo disponible tras la compra: ${cupo_disp - valor_compra:,.2f}")
                            
                    except ValueError:
                        print("[ERROR] Ingresaste un valor numérico inválido.")

            elif opcion == "10":
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