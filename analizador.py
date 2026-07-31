import os
from datetime import datetime
from palabras import PALABRAS_CLAVE
import basedatos
# Nuevo: importamos nuestro módulo de base de datos para poder guardar
# cada evento ahí, además de en el reporte de texto.


def parsear_linea(linea):
    # Función nueva. Recibe una línea como:
    # "[2026-07-23 13:10:25] [CRITICAL] IP: 172.16.254.1 - Inyección SQL detectada"
    # y la separa en sus 4 partes: fecha, severidad, ip, mensaje.
    try:
        partes = linea.split("] ", 2)
        # Divide la línea por "] " (corchete + espacio), como máximo en 3 trozos.
        # Resultado: ["[2026-07-23 13:10:25", "[CRITICAL", "IP: 172.16.254.1 - Inyección SQL detectada"]

        fecha = partes[0].replace("[", "").strip()
        # Quitamos el corchete que sobra al principio y los espacios extra.

        severidad = partes[1].replace("[", "").replace("]", "").strip()
        # Igual, quitamos los corchetes sobrantes.

        resto = partes[2]
        # resto = "IP: 172.16.254.1 - Inyección SQL detectada"

        ip_y_mensaje = resto.split(" - ", 1)
        # Separa "IP: 172.16.254.1" de "Inyección SQL detectada" por el " - ".

        ip = ip_y_mensaje[0].replace("IP:", "").strip()
        mensaje = ip_y_mensaje[1].strip() if len(ip_y_mensaje) > 1 else ""

        return fecha, severidad, ip, mensaje
        # Devolvemos las 4 partes juntas (una "tupla").

    except (IndexError, ValueError):
        # Si una línea viene rota o con formato raro, no rompemos el programa,
        # simplemente decimos "no he podido leer esta línea".
        return None


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

            hallazgos = {"CRITICAL": [], "HIGH": [], "WARNING": []}
            acciones_soar = []

            for linea in lineas:
                datos = parsear_linea(linea)
                # Intentamos extraer fecha/severidad/ip/mensaje de esta línea.
                if not datos:
                    # Línea con formato raro: no la podemos procesar de forma fiable,
                    # así que la saltamos en vez de intentar adivinar su contenido a mano.
                    continue

                fecha, severidad, ip, mensaje = datos
                basedatos.insertar_evento(fecha, severidad, ip, mensaje)
                # Guardamos el evento en la base de datos.

                if severidad == "CRITICAL":
                    criticos += 1
                    if ip:
                        acciones_soar.append(f"[BLOQUEO ACTIVO] - IP aislada por alerta crítica: {ip}")

                        print("\n" + "🚨" * 15)
                        print(f"  ALERTA CRÍTICA — IP BLOQUEADA: {ip}")
                        print("🚨" * 15 + "\n")

                        with open("firewall_block.txt", "a", encoding="utf-8") as archivo_firewall:
                            marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            archivo_firewall.write(f"{marca_tiempo} - BLOQUEO: {ip}\n")
                elif severidad == "WARNING":
                    warnings += 1
                elif severidad == "INFO":
                    infos += 1

                for categoria, lista_palabras in PALABRAS_CLAVE.items():
                    for amenaza in lista_palabras:
                        if amenaza.lower() in linea.lower():
                            if amenaza not in hallazgos[categoria]:
                                hallazgos[categoria].append(amenaza)

            tiempo_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            for categoria, lista in hallazgos.items():
                if lista:
                    reporte_texto += f"\n  [{categoria}]:\n"
                    for item in lista:
                        reporte_texto += f"    - {item}\n"

            reporte_texto += "\n-----------------------------------------\n"
            reporte_texto += "[⚡] ACCIONES DE RESPUESTA AUTOMÁTICA (SOAR):\n"
            if acciones_soar:
                for accion in set(acciones_soar):
                    reporte_texto += f"  - {accion}\n"
            else:
                reporte_texto += "  - Sin acciones de bloqueo requeridas en este ciclo.\n"

            reporte_texto += "========================================="

            print(reporte_texto)

            with open(nombre_reporte, "w", encoding="utf-8") as archivo_rep:
                archivo_rep.write(reporte_texto)

            print(f"\n[+] ¡Reporte unificado guardado con éxito en '{nombre_reporte}'!")

    except FileNotFoundError:
        print("[-] Error: No se encontró el archivo servidor.log. Ejecuta el generador primero.")


if __name__ == "__main__":
    analizar_logs()