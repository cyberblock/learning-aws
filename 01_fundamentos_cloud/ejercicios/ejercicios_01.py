# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:00:00–0:34:12: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=0s
# Apunte: apuntes/01-fundamentos-cloud.md
#
# Ejercicios 01 · Fundamentos del cloud
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 01_fundamentos_cloud --mios

# Capas de la tabla IaaS/PaaS/SaaS, de arriba (aplicación) a abajo (red)
CAPAS = [
    "aplicaciones", "datos", "runtime", "middleware", "sistema operativo",
    "virtualizacion", "servidores", "almacenamiento", "red",
]


# 1. Clasifica un servicio en "IaaS", "PaaS", "SaaS" o "FaaS".
#    Debe aceptar mayúsculas o minúsculas y espacios sobrantes ("  ec2 " -> "IaaS").
#    Servicios que tiene que reconocer: EC2, Elastic Beanstalk, Heroku, Rekognition,
#    Gmail, Dropbox, Lambda. Con un servicio desconocido lanza ValueError.
def clasificar_servicio(servicio):
    raise NotImplementedError("ejercicio 1")


# 2. ¿Quién gestiona una capa en cada modelo? Devuelve "tú" o "proveedor".
#    modelo es "on-premises", "IaaS", "PaaS" o "SaaS"; capa es un elemento de CAPAS.
#    Pista: en cada modelo tú gestionas las N primeras capas de CAPAS y el proveedor el resto
#    (on-premises: todas; IaaS: hasta el sistema operativo; PaaS: aplicaciones y datos; SaaS: ninguna).
def quien_gestiona(capa, modelo):
    raise NotImplementedError("ejercicio 2")


# 3. El ejemplo de elasticidad del vídeo: de lunes a viernes hacen falta `laborable` servidores
#    y el fin de semana `finde`. Calcula el coste de una semana (24 h/día) a `precio_hora` por servidor:
#      - "fijo": tener siempre encendidos los servidores del día de más carga
#      - "elastico": encender solo los que hacen falta cada día
#      - "ahorro": fijo - elastico
#    Devuelve un dict con esas tres claves, redondeadas a 2 decimales.
def coste_semanal(laborable, finde, precio_hora):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Debe elegir la región siguiendo los criterios del vídeo, en este orden:
#      1) cumplimiento legal: si zona_obligatoria no es None, solo valen regiones de esa zona
#      2) servicios: la región debe ofrecer TODOS los servicios pedidos
#      3) proximidad: la de menor latencia; si hay empate, la más barata
#    Devuelve el código de la región, o None si ninguna cumple.
#    Cada región es un dict: {"codigo", "zona", "latencia_ms", "precio", "servicios" (set)}.
#    La versión actual elige siempre la más barata. Tiene varios fallos: encuéntralos.
def elegir_region(regiones, zona_obligatoria, servicios):
    mejor = min(regiones, key=lambda r: r["precio"])
    return mejor["codigo"]
