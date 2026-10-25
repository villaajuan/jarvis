from datetime import datetime

texto_fecha = "2026-10-23 19:22:00"
formato = "%Y-%m-%d %H:%M:%S"

# Convertir el string a objeto datetime
fecha_objeto = datetime.strptime(texto_fecha, formato)

print(type(fecha_objeto)) 
# Salida: <class 'datetime.datetime'>

print(fecha_objeto.year)
# Salida: 2026


