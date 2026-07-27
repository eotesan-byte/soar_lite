import os
from datetime import datetime
from palabras import PALABRAS_CLAVE

def analizar_logs():
    nombre_archivo = "servidor.log"
    nombre_reporte = "reporte_seguridad.txt"
    print(f"\n[+] Leyendo el archivo '{nombre_archivo}' para análisis y respuesta SOAR...")
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo_log:
            lineas = archivo_log.readlines()
            
            total_logs = len(lineas)
            criticos = 0
            warnings = 0
            infos = 0
            
            # Estructura para clasificar hallazgos según el catálogo
            hallazgos = {
                "CRITICAL": [],
                "HIGH": [],
                "WARNING": []
            }

            # Acciones de respuesta automatizada simuladas (Playbooks)
            acciones_soar = []

            for linea in lineas:
                # Conteo general de niveles tradicionales
                if "CRITICAL" in linea: 
                    criticos += 1
                    # Simulación de Playbook SOAR: Aislamiento automático ante crítico
                    if "IP:" in linea:
                        partes = linea.split("IP:")
                        if len(partes) > 1:
                            ip_detectada = partes[1].split("-")[0].strip()
                            acciones_soar.append(f"[BLOQUEO ACTIVO] - IP aislada por alerta crítica: {ip_detectada}")
                elif "WARNING" in linea:
                    warnings += 1
                elif "INFO" in linea:
                    infos += 1
                
                # Búsqueda detallada cruzando con el catálogo de palabras.py
                for categoria, lista_palabras in PALABRAS_CLAVE.items():
                    for amenaza in lista_palabras:
                        if amenaza.lower() in linea.lower():
                            if amenaza not in hallazgos[categoria]:
                                hallazgos[categoria].append(amenaza)

            tiempo_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # --- ÚNICO REPORTE UNIFICADO SOC-SOAR ---
            reporte_texto = f"""=========================================
      REPORTE INTEGRAL SOC-SOAR LITE     
=========================================
[*] Fecha del reporte               : {tiempo_reporte}
[*] Total de registros analizados : {total_logs}
[i] Eventos informativos (INFO)   : {infos}
[!] Advertencias (WARNING)        : {warnings}
[X] Incidentes críticos (CRITICAL): {criticos}
-----------------------------------------
[🔍] AMENAZAS ESPECÍFICAS DETECTADAS:
"""
            # Añadimos al reporte las amenazas concretas del catálogo
            for categoria, lista in hallazgos.items():
                if lista:
                    reporte_texto += f"\n  [{categoria}]:\n"
                    for item in lista:
                        reporte_texto += f"    - {item}\n"

            # Añadimos la sección de automatización de respuesta (Playbooks ejecutados)
            reporte_texto += "\n-----------------------------------------\n"
            reporte_texto += "[⚡] ACCIONES DE RESPUESTA AUTOMÁTICA (SOAR):\n"
            if acciones_soar:
                for accion in set(acciones_soar):  # Usamos set para evitar duplicados exactos en el reporte
                    reporte_texto += f"  - {accion}\n"
            else:
                reporte_texto += "  - Sin acciones de bloqueo requeridas en este ciclo.\n"

            reporte_texto += "========================================="

            # 1. Imprimimos el reporte consolidado por pantalla
            print(reporte_texto)
            
            # 2. Guardamos el reporte único en el archivo estándar
            with open(nombre_reporte, "w", encoding="utf-8") as archivo_rep:
                archivo_rep.write(reporte_texto)
                
            print(f"\n[+] ¡Reporte unificado guardado con éxito en '{nombre_reporte}'!")
            
    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo servidor.log. Ejecuta el generador primero.")

if __name__ == "__main__":
    analizar_logs()