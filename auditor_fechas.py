import time
from datetime import datetime, timedelta

def analizar_registro(fecha_texto):
    print("Iniciando análisis de datos...")
    
    # Inicia el cronómetro
    inicio_reloj = time.perf_counter()

    # Convierte el texto a datetime
    fecha_registro = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M:%S")
    
    # Obtiene la hora actual
    ahora = datetime.now()
    
    # Calcula la diferencia y extrae los días
    tiempo_transcurrido = ahora - fecha_registro
    dias_pasados = tiempo_transcurrido.days
    
    # Proyecta 30 días al futuro
    fecha_vencimiento = fecha_registro + timedelta(days=30)
    
    # Extrae la semana ISO
    año_iso, semana_iso, dia_iso = fecha_registro.isocalendar()

    # Detiene el cronómetro
    fin_reloj = time.perf_counter()
    tiempo_ejecucion = fin_reloj - inicio_reloj

    # Imprime el reporte
    print("\n" + "="*35)
    print(" 📊 REPORTE DE TIEMPOS DEL SISTEMA")
    print("="*35)
    print(f"🔹 Fecha original       : {fecha_registro.strftime('%d/%b/%Y %I:%M %p')}")
    print(f"🔹 Semana ISO           : Semana {semana_iso} del {año_iso}")
    print(f"🔹 Días transcurridos   : {dias_pasados} días")
    print(f"🔹 Proyección a 30 días : {fecha_vencimiento.strftime('%d/%b/%Y')}")
    print("-" * 35)
    print(f"⏱️ [Debug] Tiempo CPU   : {tiempo_ejecucion:.6f} segundos")
    print("="*35 + "\n")

# Ejecución de la prueba
texto_del_log = "2026-06-14 00:00:00"
analizar_registro(texto_del_log)