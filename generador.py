import random
import os
from datetime import datetime  # <--- Para sacar la fecha y hora actual
import palabras

def generar_logs():
    nombre_archivo = "servidor.log"
    cantidad_logs = 10
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        for _ in range(cantidad_logs):
            ip = random.choice(palabras.LISTA_IPS)
            nivel = random.choice(palabras.NIVELES_SEVERIDAD)
            
            # Obtenemos la fecha y hora actual formateada
            tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if nivel == "INFO":
                mensaje = random.choice(palabras.MENSAJES_INFO)
            elif nivel == "WARNING":
                mensaje = random.choice(palabras.MENSAJES_WARNING)
            else:
                mensaje = random.choice(palabras.MENSAJES_CRITICAL)
                
            # Escribimos el log incluyendo la marca de tiempo
            f.write(f"[{tiempo_actual}] [{nivel}] IP: {ip} - {mensaje}\n")
            
    ruta_absoluta = os.path.abspath(nombre_archivo)
    print(f"[+] --- ¡ARCHIVO '{nombre_archivo}' GENERADO CON ÉXITO! ---")
    print(f"[i] Ruta de almacenamiento: {ruta_absoluta}")
