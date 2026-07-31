import generador
import analizador
import basedatos
import agente

def mostrar_menu():
    print("\n=========================================")
    print("        SOAR-LITE — MENÚ PRINCIPAL        ")
    print("=========================================")
    print("1. Generar logs nuevos")
    print("2. Ejecutar analizador")
    print("3. Ejecutar agente (puertos + software)")
    print("4. Ver histórico de eventos")
    print("5. Salir")

def ver_historico():
    eventos = basedatos.obtener_ultimos_eventos()
    if not eventos:
        print("[-] No hay eventos guardados todavía.")
        return
    print("\n--- Últimos eventos registrados ---")
    for fecha, severidad, ip, mensaje in eventos:
        print(f"[{fecha}] [{severidad}] IP: {ip} - {mensaje}")

def main():
    basedatos.crear_tabla()
    basedatos.crear_tablas_agente()
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            generador.generar_logs()
        elif opcion == "2":
            analizador.analizar_logs()
        elif opcion == "3":
            reporte = agente.generar_reporte()
            fecha_nueva = basedatos.guardar_reporte_en_bd(reporte)
            basedatos.limpiar_historico_antiguo()
            print(f"Puertos: {len(reporte['puertos_abiertos'])} | Software: {len(reporte['software_instalado'])}")

            anomalias_puertos = basedatos.detectar_anomalias("puertos", fecha_nueva)
            for puerto, protocolo, proceso in anomalias_puertos:
                if proceso == "desconocido":
                    severidad = "WARNING"
            else:
                severidad = "INFO"
                mensaje = f"Nuevo puerto abierto: {puerto}/{protocolo} (proceso: {proceso})"
                basedatos.insertar_evento(fecha_nueva, severidad, None, mensaje)

                anomalias_software = basedatos.detectar_anomalias("software", fecha_nueva)
                for nombre, version in anomalias_software:
                    mensaje = f"Nuevo software instalado: {nombre} {version}"
                    basedatos.insertar_evento(fecha_nueva, "INFO", None, mensaje)

                total = len(anomalias_puertos) + len(anomalias_software)
            if total > 0:
             print(f"[!] Anomalías detectadas: {len(anomalias_puertos)} puertos nuevos, {len(anomalias_software)} programas nuevos")
            else:
             print("[+] Sin cambios respecto al snapshot anterior.")
      
        elif opcion == "4":
            ver_historico()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("[-] Opción no válida, prueba otra vez.")
            continue

        input("\nPulsa Enter para volver al menú...")
 

if __name__ == "__main__":
    main()