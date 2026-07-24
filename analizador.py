import os
from datetime import datetime
def analizar_logs():
    nombre_archivo = "servidor.log"
    nombre_reporte = "reporte seguridad.txt"
    print(f"\n[+] Leyendo el archivo '{nombre_archivo}' para buscar amenazas...")
    
    try:
        with open("servidor.log", "r", encoding="utf-8") as archivo_log:
            lineas = archivo_log.readlines()
            
            total_logs = len(lineas)
            criticos = 0
            warnings = 0
            infos =0
            for linea in lineas:
                if "CRITICAL" in linea: 
                    criticos += 1
                elif "WARNING" in linea:
                    warnings +=1
                elif "INFO" in linea:
                    infos +=1
            
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
========================================="""

# 1. Imprimimos el reporte por pantalla
            print(reporte_texto)
            
            # 2. Guardamos el reporte en el archivo de texto
            with open(nombre_reporte, "w", encoding="utf-8") as archivo_rep:
                archivo_rep.write(reporte_texto)
                
            print(f"[+] ¡Reporte guardado con éxito en '{nombre_reporte}'!")
            
    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo servidor.log. Ejecuta el generador primero.")
