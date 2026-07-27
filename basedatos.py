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
    # Abrimos la conexión a la base de datos.

    cursor = conexion.cursor()
    # El "cursor" es como el bolígrafo con el que escribimos/leemos en la BD.
    # Toda instrucción SQL se ejecuta a través de él.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            severidad TEXT,
            ip TEXT,
            mensaje TEXT
        )
    """)
    # "CREATE TABLE IF NOT EXISTS" crea la tabla solo si aún no existe,
    # así puedes ejecutar esta función cada vez sin que dé error.
    # "id INTEGER PRIMARY KEY AUTOINCREMENT" crea un número único
    # que se genera solo para cada fila (fila 1, fila 2, fila 3...).

    conexion.commit()
    # "commit" guarda de verdad los cambios en el archivo .db.
    # Sin esto, la creación de la tabla se quedaría solo "en memoria"
    # y se perdería al cerrar el programa.

    conexion.close()
    # Cerramos la conexión, buena práctica para no dejarla abierta sin usar.


def insertar_evento(fecha, severidad, ip, mensaje):
    # Esta función guarda un evento nuevo en la tabla.
    # Los cuatro parámetros son los datos de ese evento.
    conexion = crear_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO eventos (fecha, severidad, ip, mensaje) VALUES (?, ?, ?, ?)",
        (fecha, severidad, ip, mensaje)
    )
    # "INSERT INTO eventos (...) VALUES (...)" añade una fila nueva.
    # Los signos "?" son "huecos" que se rellenan con la tupla de después.
    # IMPORTANTE: nunca metas los valores directamente en el texto SQL
    # (tipo f-string) porque es inseguro; los "?" evitan ese problema
    # (se llama "SQL injection", ¡el mismo ataque que tienes en palabras.py!).

    conexion.commit()
    # Guardamos el cambio de verdad en el archivo.

    conexion.close()
    # Cerramos la conexión.