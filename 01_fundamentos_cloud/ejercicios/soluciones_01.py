# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:00:00–0:34:12: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=0s
# Apunte: apuntes/01-fundamentos-cloud.md
#
# Soluciones 01 · Fundamentos del cloud

CAPAS = [
    "aplicaciones", "datos", "runtime", "middleware", "sistema operativo",
    "virtualizacion", "servidores", "almacenamiento", "red",
]

MODELO_DE_SERVICIO = {
    "ec2": "IaaS",
    "elastic beanstalk": "PaaS",
    "heroku": "PaaS",
    "rekognition": "SaaS",
    "gmail": "SaaS",
    "dropbox": "SaaS",
    "lambda": "FaaS",
}

# Número de capas (desde arriba) que gestionas tú en cada modelo
CAPAS_PROPIAS = {"on-premises": 9, "IaaS": 5, "PaaS": 2, "SaaS": 0}


# 1.
def clasificar_servicio(servicio):
    clave = servicio.strip().lower()
    if clave not in MODELO_DE_SERVICIO:
        raise ValueError(f"servicio desconocido: {servicio!r}")
    return MODELO_DE_SERVICIO[clave]


# 2.
def quien_gestiona(capa, modelo):
    return "tú" if CAPAS.index(capa) < CAPAS_PROPIAS[modelo] else "proveedor"


# 3.
def coste_semanal(laborable, finde, precio_hora):
    fijo = max(laborable, finde) * 7 * 24 * precio_hora
    elastico = (laborable * 5 + finde * 2) * 24 * precio_hora
    return {
        "fijo": round(fijo, 2),
        "elastico": round(elastico, 2),
        "ahorro": round(fijo - elastico, 2),
    }


# 4. Fallos de la versión original:
#    - ignoraba la zona obligatoria (requisitos legales)
#    - ignoraba si la región ofrece los servicios necesarios
#    - ordenaba por precio en lugar de por latencia (el precio solo desempata)
#    - con una lista vacía (o sin candidatas) min() lanzaba ValueError en vez de devolver None
def elegir_region(regiones, zona_obligatoria, servicios):
    candidatas = [
        r for r in regiones
        if (zona_obligatoria is None or r["zona"] == zona_obligatoria)
        and set(servicios) <= r["servicios"]
    ]
    if not candidatas:
        return None
    mejor = min(candidatas, key=lambda r: (r["latencia_ms"], r["precio"]))
    return mejor["codigo"]
