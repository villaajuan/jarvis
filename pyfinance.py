import json
from datetime import datetime

print("Iniciando motor de pyfinance...\n")

# 1. Ruta exacta al archivo JSON
ruta = "data/datos_finanzas.json"

# 2. Abrir y cargar el archivo
with open(ruta, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

# 3. Extraer los textos de las fechas
texto_bancolombia = datos["bancolombia"]["ultima_actualizacion"]
texto_lulo = datos["lulo_bank"]["ultima_actualizacion"]
texto_nu = datos["tarjeta_nu"]["fecha_proximo_corte"]

# 4. Convertir los textos a objetos datetime
formato = "%Y-%m-%d %H:%M:%S"
fecha_bancolombia = datetime.strptime(texto_bancolombia, formato)
fecha_lulo = datetime.strptime(texto_lulo, formato)
fecha_nu = datetime.strptime(texto_nu, formato)
ahora = datetime.now()

# 5. Calcular los días de diferencia
dias_bancolombia = (ahora - fecha_bancolombia).days
dias_lulo = (ahora - fecha_lulo).days
dias_nu = (fecha_nu - ahora).days

# 6. Imprimir el panel de control
print("📊 PANEL FINANCIERO CENTRAL")
print("-" * 40)
print(f"🏦 Bancolombia : Sin actualizar hace {dias_bancolombia} días.")
print(f"🟣 Lulo Bank   : Sin actualizar hace {dias_lulo} días.")
print(f"💳 Tarjeta Nu  : Faltan {dias_nu} días para el corte.")
print("-" * 40)
# 7. Menú interactivo para actualizar datos
print("\nOpciones de actualización:")
actualizar = input("¿Deseas actualizar la fecha de Bancolombia al día de hoy? (s/n): ")

if actualizar.lower() == 's':
    # 1. Modificamos el dato en la memoria de Python (usando la fecha de hoy)
    datos["bancolombia"]["ultima_actualizacion"] = ahora.strftime(formato)
    
    # 2. Sobrescribimos el archivo JSON con los datos actualizados
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)
        
    print("✅ Base de datos actualizada: Bancolombia quedó registrado con la fecha y hora actuales.")
else:
    print("Saliendo del sistema. No se realizaron cambios.")
