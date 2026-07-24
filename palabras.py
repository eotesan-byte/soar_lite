NIVELES_SEVERIDAD = ["INFO" , "WARNING", "CRITICAL"]

# IPs de prueba (algunas normales y otras con pinta de sospechosas)
LISTA_IPS = [
    "192.168.1.10",
    "192.168.1.45",
    "10.0.0.15",
    "203.0.113.42",
    "198.51.100.23",
    "172.16.254.1"
]

# Mensajes normales de rutina (INFO)
MENSAJES_INFO = [
    "Usuario autenticado correctamente",
    "Página principal cargada con éxito",
    "Cierre de sesión de usuario",
    "Consulta realizada a la base de datos sin incidencias"
]

# Mensajes de advertencia (WARNING)
MENSAJES_WARNING = [
    "Intento de acceso con credenciales incorrectas",
    "Puerto no autorizado escaneado",
    "Alto uso de memoria detectado en el servicio web"
]

# Mensajes críticos / ataques (CRITICAL)
MENSAJES_CRITICAL = [
    "Inyección SQL detectada en el parámetro de entrada",
    "Ataque de fuerza bruta masivo en curso",
    "Desbordamiento de búfer detectado en el puerto 80",
    "Acceso no autorizado a directorio raíz"
]