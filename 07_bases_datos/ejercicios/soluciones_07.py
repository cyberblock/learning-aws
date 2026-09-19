# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 2:41:29–3:18:56: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9689s
# Apunte: apuntes/07-bases-de-datos.md
#
# Soluciones de los ejercicios 07 · Bases de datos (RDS, Aurora y DynamoDB)

import re

PERMITIDOS = re.compile(r"^[A-Za-z0-9_.-]+$")


def tipo_de_base_de_datos(caso):
    pistas = ("consultas_sql", "esquema_fijo", "relaciones")
    if any(caso.get(pista) for pista in pistas):
        return "relacional"
    return "no relacional"


def item_dynamodb(datos):
    item = {}
    for clave, valor in datos.items():
        if valor is None:
            item[clave] = {"NULL": True}
        elif isinstance(valor, bool):          # antes que int: bool hereda de int
            item[clave] = {"BOOL": valor}
        elif isinstance(valor, str):
            item[clave] = {"S": valor}
        elif isinstance(valor, (int, float)):
            item[clave] = {"N": str(valor)}
        else:
            raise TypeError(f"tipo no soportado para {clave}: {type(valor).__name__}")
    return item


def nombre_tabla_valido(nombre):
    return bool(3 <= len(nombre) <= 255 and PERMITIDOS.match(nombre))


def atributos(items):
    nombres = set()
    for item in items:
        nombres.update(item.keys())
    return sorted(nombres)
