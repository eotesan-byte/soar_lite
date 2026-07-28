# basedatos.py
# Este módulo se encarga de todo lo relacionado con guardar y leer datos
# en la base de datos SQLite. Así centralizamos aquí toda la lógica de BD,
# y el resto del programa no necesita saber cómo funciona SQL por dentro.

import sqlite3
# Importamos el módulo sqlite3, que viene incluido con Python.
# Nos da las herramientas para crear/abrir un archivo .db y hablar con él.

NOMBRE_BD = "soar.db"
# Guardamos el nombre del archivo de base de datos en una variable.
# Así, si algún día lo quieres cambiar, solo lo tocas aquí una vez.


def crear_conexion():
    # Esta función abre (o crea, si no existe) el archivo soar.db
    # y devuelve un objeto "conexión" que usaremos para hablar con la BD.
    conexion = sqlite3.connect(NOMBRE_BD)
    return conexion


def crear_tabla():
    # Esta función se asegura de que la tabla "eventos" exista.
    # La llamaremos una vez al arrancar el programa.
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
    # Esta función guarda un evento nuevo en la tabla.
    # Los cuatro parámetros son los datos de ese evento.
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO eventos (fecha, severidad, ip, mensaje) VALUES (?, ?, ?, ?)",
        (fecha, severidad, ip, mensaje)
    )

    conexion.commit()
    conexion.close()


def crear_tablas_agente():
    # Igual que crear_tabla(), pero para las tablas de puertos y software.
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puertos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puerto INTEGER,
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
    from datetime import datetime

    conexion = crear_conexion()
    cursor = conexion.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for puerto in reporte["puertos_abiertos"]:
        cursor.execute(
            "INSERT INTO puertos (puerto, fecha) VALUES (?, ?)",
            (puerto, ahora)
        )

    for programa in reporte["software_instalado"]:
        cursor.execute(
            "INSERT INTO software (nombre, version, fecha) VALUES (?, ?, ?)",
            (programa["nombre"], programa["version"], ahora)
        )

    conexion.commit()
    conexion.close()