import os
from datetime import datetime
from palabras import PALABRAS_CLAVE

def analizar_logs():
    nombre_archivo = "servidor.log"
    nombre_reporte = "reporte seguridad.txt"
    print(f"\n[+] Leyendo el archivo '{nombre_archivo}' para buscar amenazas del catálogo...")
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo_log:
            lineas = archivo_log.readlines()
            
            total_logs = len(lineas)
            criticos = 0
            warnings = 0
            infos = 0
            
            # Diccionario para llevar la cuenta de qué amenazas específicas van apareciendo
            hallazgos = {
                "CRITICAL": [],
                "HIGH": [],
                "WARNING": []
            }

            for linea in lineas:
                # Conteo general basado en los niveles tradicionales que ya tenías
                if "CRITICAL" in linea: 
                    criticos += 1
                elif "WARNING" in linea:
                    warnings +=1
                elif "INFO" in linea:
                    infos +=1
                
                # Búsqueda detallada cruzando con el catálogo de palabras.py
                for categoria, lista_palabras in PALABRAS_CLAVE.items():
                    for amenaza in lista_palabras:
                        if amenaza.lower() in linea.lower():
                            # Guardamos la coincidencia si no la teníamos duplicada exactamente en esa línea
                            if amenaza not in hallazgos[categoria]:
                                hallazgos[categoria].append(amenaza)

            tiempo_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # --- REPORTE DE SEGURIDAD SOC ---
            reporte_texto = f"""=========================================
         REPORTE DE SEGURIDAD SOC        
=========================================
[*] Fecha del reporte               : {tiempo_reporte}
[*] Total de registros analizados : {total_logs}
[i] Eventos informativos (INFO)   : {infos}
[!] Advertencias (WARNING)        : {warnings}
[X] Incidentes críticos (CRITICAL): {criticos}
-----------------------------------------
[🔍] AMENAZAS ESPECÍFICAS DETECTADAS:
"""
            # Añadimos al reporte las amenazas concretas que se han encontrado
            for categoria, lista in hallazgos.items():
                if lista:
                    reporte_texto += f"\n  [{categoria}]:\n"
                    for item in lista:
                        reporte_texto += f"    - {item}\n"

            reporte_texto += "========================================="

            # 1. Imprimimos el reporte por pantalla
            print(reporte_texto)
            
            # 2. Guardamos el reporte en el archivo de texto
            with open(nombre_reporte, "w", encoding="utf-8") as archivo_rep:
                archivo_rep.write(reporte_texto)
                
            print(f"[+] ¡Reporte guardado con éxito en '{nombre_reporte}'!")
            
    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo servidor.log. Ejecuta el generador primero.")

if __name__ == "__main__":
    analizar_logs()
    