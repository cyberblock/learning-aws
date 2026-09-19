# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 2:27:32–2:41:29: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8852s
# Apunte: apuntes/06-s3.md
#
# Soluciones de los ejercicios 06 · Almacenamiento de objetos (S3)

import re

GIB = 1024 ** 3
TIB = 1024 ** 4
MAXIMO_SIMPLE = 5 * GIB
MAXIMO_OBJETO = 5 * TIB

PERMITIDOS = re.compile(r"^[a-z0-9.-]+$")
ES_IP = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def nombre_valido(nombre):
    if not 3 <= len(nombre) <= 63:
        return False
    if not PERMITIDOS.match(nombre):
        return False
    if not (nombre[0].isalnum() and nombre[-1].isalnum()):
        return False
    if ES_IP.match(nombre):
        return False
    if nombre.startswith("xn--") or nombre.endswith("-s3alias"):
        return False
    return True


def partir_clave(clave):
    if "/" not in clave:
        return "", clave
    prefijo, _, nombre = clave.rpartition("/")
    return prefijo + "/", nombre


def forma_de_subida(bytes_objeto):
    if bytes_objeto > MAXIMO_OBJETO:
        raise ValueError("un objeto de S3 no puede pasar de 5 TiB")
    return "multiparte" if bytes_objeto > MAXIMO_SIMPLE else "simple"


def objetos_directos(claves, prefijo):
    directos = []
    for clave in claves:
        if not clave.startswith(prefijo):
            continue
        resto = clave[len(prefijo):]
        if resto and "/" not in resto:
            directos.append(clave)
    return directos
