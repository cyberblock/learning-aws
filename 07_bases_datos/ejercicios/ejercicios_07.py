# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 2:41:29–3:18:56: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9689s
# Apunte: apuntes/07-bases-de-datos.md
#
# Ejercicios 07 · Bases de datos (RDS, Aurora y DynamoDB)
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 07_bases_datos --mios


# 1. ¿Relacional o no relacional? Decide a partir de las pistas del caso:
#       {"consultas_sql": True, "esquema_fijo": True, "relaciones": True}
#    Devuelve "relacional" si hay consultas SQL, esquema fijo o relaciones entre tablas;
#    devuelve "no relacional" en cualquier otro caso (datos JSON anidados, esquema que
#    cambia con el tiempo, clave-valor).
def tipo_de_base_de_datos(caso):
    raise NotImplementedError("ejercicio 1")


# 2. Convierte un dict de Python al formato de atributos de DynamoDB:
#       str   -> {"S": valor}
#       bool  -> {"BOOL": valor}      ¡ojo!, en Python bool es subclase de int
#       int y float -> {"N": "valor como texto"}
#       None  -> {"NULL": True}
#    item_dynamodb({"nombre": "Joan", "edad": 30}) ->
#       {"nombre": {"S": "Joan"}, "edad": {"N": "30"}}
#    Con cualquier otro tipo, lanza TypeError.
def item_dynamodb(datos):
    raise NotImplementedError("ejercicio 2")


# 3. ¿Es válido el nombre de una tabla de DynamoDB? De 3 a 255 caracteres y solo
#    letras, números, guion bajo, guion normal y punto.
def nombre_tabla_valido(nombre):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Devuelve, ordenados alfabéticamente, todos los nombres de
#    atributo que aparecen en una tabla NoSQL. Recuerda que cada elemento puede tener
#    atributos distintos: no todos los elementos comparten el mismo esquema.
#    items = [{"user_id": 1, "nombre": "Joan"}, {"user_id": 2, "apellido": "Amengual"}]
#    atributos(items) -> ["apellido", "nombre", "user_id"]
def atributos(items):
    if not items:
        return []
    return sorted(items[0].keys())
