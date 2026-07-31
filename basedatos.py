import sqlite3
from datetime import datetime, timedelta

NOMBRE_BD = "soar.db"


def crear_conexion():
    conexion = sqlite3.connect(NOMBRE_BD)
    return conexion


def crear_tabla():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            severidad TEXT,
            ip TEXT,
            mensaje TEXT
        )
    """)

    conexion.commit()
    conexion.close()


def insertar_evento(fecha, severidad, ip, mensaje):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO eventos (fecha, severidad, ip, mensaje) VALUES (?, ?, ?, ?)",
        (fecha, severidad, ip, mensaje)
    )

    conexion.commit()
    conexion.close()


def crear_tablas_agente():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puertos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puerto INTEGER,
            protocolo TEXT,
            proceso TEXT,
            fecha TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            version TEXT,
            fecha TEXT
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_reporte_en_bd(reporte):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for puerto in reporte["puertos_abiertos"]:
        cursor.execute(
            "INSERT INTO puertos (puerto, protocolo, proceso, fecha) VALUES (?, ?, ?, ?)",
            (puerto["puerto"], puerto["protocolo"], puerto["proceso"], ahora)
        )

    for programa in reporte["software_instalado"]:
        cursor.execute(
            "INSERT INTO software (nombre, version, fecha) VALUES (?, ?, ?)",
            (programa["nombre"], programa["version"], ahora)
        )

    conexion.commit()
    conexion.close()
    return ahora


def limpiar_historico_antiguo():
    conexion = crear_conexion()
    cursor = conexion.cursor()

    limite = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("DELETE FROM puertos WHERE fecha < ?", (limite,))
    cursor.execute("DELETE FROM software WHERE fecha < ?", (limite,))

    conexion.commit()
    conexion.close()


def obtener_snapshot(tabla, fecha):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    if tabla == "puertos":
        cursor.execute("SELECT puerto, protocolo, proceso FROM puertos WHERE fecha = ?", (fecha,))
    else:
        cursor.execute("SELECT nombre, version FROM software WHERE fecha = ?", (fecha,))
    resultados = cursor.fetchall()
    conexion.close()
    # set() quita duplicados exactos automáticamente (por ejemplo, un
    # mismo programa que a veces aparece registrado dos veces en el
    # registro de Windows con el mismo nombre y versión).
    return set(resultados)

def obtener_ultima_fecha(tabla):
    conexion =crear_conexion()
    cursor = conexion.cursor()
    if tabla == "puertos":
        cursor.execute(
        "SELECT DISTINCT fecha FROM puertos ORDER BY fecha DESC LIMIT 2"
        )
    else:
        cursor.execute(
        "SELECT DISTINCT fecha FROM software ORDER BY fecha DESC LIMIT 2"
        )
       
    
    resultados = cursor.fetchall()
    conexion.close()    
    resultados = cursor.fetchall()
    conexion.close()
    if len(resultados) < 2:
        return None
    else:
        return resultados[1][0]

def detectar_anomalias(tabla, fecha_nueva):
    fecha_anterior = obtener_ultima_fecha(tabla)
    if fecha_anterior is None:
        return set()
    snapshot_anterior = obtener_snapshot(tabla, fecha_anterior)
    snapshot_nuevo = obtener_snapshot(tabla, fecha_nueva)
    nuevos_elementos = snapshot_nuevo - snapshot_anterior
    return nuevos_elementos

def obtener_ultimos_eventos(limite=10):
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT fecha, severidad, ip, mensaje FROM eventos ORDER BY id DESC LIMIT ?",
        (limite,)
    )
    resultados = cursor.fetchall()
    conexion.close()
    return resultados




    
