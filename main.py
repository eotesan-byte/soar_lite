# Importamos nuestros módulos
import generador
import analizador
import basedatos

def main():
    basedatos.crear_tabla()
    print("=========================================")
    print("   INICIANDO SIMULADOR SOC - SOAR LITE   ")
    print("=========================================")
    
    # Paso 1: Llamamos al generador de tráfico/logs
    generador.generar_logs()
    
    # Paso 2: Llamamos al analizador de seguridad
    analizador.analizar_logs()
    
    print("\n=========================================")
    print("   CICLO DE SIMULACIÓN FINALIZADO        ")
    print("=========================================")

if __name__ == "__main__":
    main()
