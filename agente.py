import psutil 
import winreg #registro windows 

def listar_puertos_abiertos():
    conexiones = psutil.net_connections(kind='inet') #nos da una lista de conexiones delde red del sistema
    puertos = []
    for conexion in conexiones:
        if conexion.status == 'LISTEN':  #filtramos solo puertos abiertos, es decir los ueestan escuchando
            puertos.append(conexion.laddr.port) #local addres, sacamos el numero de puerto
    return puertos


def listar_software_instalado():
    rutas_registro = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    software = []

    for ruta in rutas_registro:
        try:
            clave_principal = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta)
        except FileNotFoundError:
            continue

        total_subclaves = winreg.QueryInfoKey(clave_principal)[0]

        for i in range(total_subclaves):
            try:
                nombre_subclave = winreg.EnumKey(clave_principal, i)
                subclave = winreg.OpenKey(clave_principal, nombre_subclave)
                nombre = winreg.QueryValueEx(subclave, "DisplayName")[0]
                try:
                    version = winreg.QueryValueEx(subclave, "DisplayVersion")[0]
                except FileNotFoundError:
                    version = "desconocida"
                software.append((nombre, version))
            except (FileNotFoundError, OSError):
                continue

    return software



import json

def generar_reporte():
    reporte = {
        "puertos_abiertos": listar_puertos_abiertos(),
        "software_instalado": [
            {"nombre": nombre, "version": version}
            for nombre, version in listar_software_instalado()
        ]
    }
    return reporte

if __name__ == "__main__":
    reporte = generar_reporte()

    with open("reporte_agente.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)

    print(f"Puertos encontrados: {len(reporte['puertos_abiertos'])}")
    print(f"Software encontrado: {len(reporte['software_instalado'])}")
    print("Reporte guardado en reporte_agente.json")


