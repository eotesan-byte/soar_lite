# Catálogo de amenazas realistas para el motor SOC-SOAR Lite
# Comentarios orientativos para el analista (significado e impacto operativo)

PALABRAS_CLAVE = {
    "CRITICAL": [
        "SQL injection",          # Inyección de código malicioso en bases de datos para robar o alterar info.
        "Remote Code Execution",  # Permite al atacante ejecutar comandos de forma remota en el sistema.
        "Unauthorized root access",# Acceso ilícito con privilegios máximos de administrador.
        "Malware signature matched",# Coincidencia confirmada con una firma de troyano o código malicioso.
        "Reverse shell established",# Conexión saliente maliciosa que otorga una consola de comandos interactiva.
        "Mass file modification"    # Patrón típico de ransomware cifrando carpetas masivamente.
    ],
    "HIGH": [
        "Failed password for root",       # Intentos repetidos de fuerza bruta a la cuenta del superusuario.
        "Failed password for invalid user",# Intentos de login usando usuarios que ni existen en el sistema.
        "Directory traversal",             # Intento de navegar por directorios no autorizados del servidor.
        "/etc/passwd",                     # Acceso al fichero de usuarios Linux buscando cuentas para ataques.
        "admin/config.php",                # Localización de paneles de control o ficheros de configuración web.
        "Privilege escalation attempt",    # Maniobras para elevar permisos a administrador desde una cuenta baja.
        "PowerShell hidden execution",     # Uso de scripts de consola ocultos para descargar cargas maliciosas.
        "Suspicious outbound connection"   # Tráfico saliente a IPs/puertos extraños (posible exfiltración).
    ],
    "WARNING": [
        "Port scan detected",          # Sondeo masivo de puertos para ver qué servicios están abiertos.
        "Multiple connection retries", # Intentos constantes de conexión que pueden saturar un servicio.
        "HTTP 403 Forbidden",          # Peticiones denegadas por falta de permisos (rastreo de directorios).
        "High CPU utilization",        # Picos anormales de procesador (típico de bucles o minería oculta).
        "Anonymous login",             # Acceso anónimo permitido a servicios críticos como FTP.
        "Rate limit exceeded",         # Superación de peticiones permitidas (ataques de fuerza bruta/bots).
        "DDoS attack mitigated",       # Denegación de servicio distribuido bloqueada por perimetrales.
        "Suspicious redirect",         # Redirección web maliciosa hacia sitios de phishing.
        "File dropped in temp"         # Creación de ejecutables en carpetas temporales (infección inicial).
    ]
}
LISTA_IPS = [
    "192.168.1.10",
    "10.0.0.15",
    "172.16.254.1",
    "198.51.100.23",
    "203.0.113.42"
]
# IPs de ejemplo (de rangos reservados para pruebas, no son IPs reales de nadie).

NIVELES_SEVERIDAD = ["INFO", "WARNING", "CRITICAL"]
# Los tres niveles que generador.py elige al azar para cada log.

MENSAJES_INFO = [
    "Acceso permitido usuario: admin",
    "Cierre de sesión de usuario",
    "Servicio reiniciado correctamente"
]

MENSAJES_WARNING = [
    "Intento de acceso con credenciales incorrectas",
    "Puerto no autorizado escaneado",
    "Alto uso de memoria detectado en el servicio web"
]

MENSAJES_CRITICAL = [
    "Inyección SQL detectada en el parámetro de entrada",
    "Desbordamiento de búfer detectado en el puerto 80",
    "Acceso root no autorizado detectado"
]