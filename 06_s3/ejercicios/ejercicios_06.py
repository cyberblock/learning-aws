# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 2:27:32–2:41:29: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8852s
# Apunte: apuntes/06-s3.md
#
# Ejercicios 06 · Almacenamiento de objetos (S3)
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 06_s3 --mios


# 1. ¿Es válido el nombre de un bucket de uso general? Reglas:
#    - de 3 a 63 caracteres;
#    - solo minúsculas, números, puntos y guiones (nada de mayúsculas ni guion bajo);
#    - empieza y termina por letra minúscula o número;
#    - no puede ser una dirección IPv4 (por ejemplo "192.168.1.1");
#    - no empieza por "xn--" ni termina en "-s3alias".
def nombre_valido(nombre):
    raise NotImplementedError("ejercicio 1")


# 2. Parte una clave de objeto en (prefijo, nombre). El prefijo incluye la barra final;
#    si la clave no tiene barras, el prefijo es "".
#    partir_clave("mi-carpeta/otra/mi-archivo.txt") -> ("mi-carpeta/otra/", "mi-archivo.txt")
def partir_clave(clave):
    raise NotImplementedError("ejercicio 2")


# 3. ¿Cómo hay que subir un objeto de `bytes`? Devuelve:
#    - "simple" si cabe en una subida normal (hasta 5 GiB);
#    - "multiparte" si pasa de 5 GiB y no supera el máximo por objeto (5 TiB);
#    - lanza ValueError si supera el máximo.
#    1 GiB = 1024**3 bytes.
def forma_de_subida(bytes_objeto):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Devuelve los objetos que están DIRECTAMENTE dentro de una
#    "carpeta" (un prefijo), sin entrar en las subcarpetas. Recuerda que en S3 no hay
#    directorios: solo claves con barras.
#    claves = ["a.txt", "images/b.jpg", "images/sub/c.jpg"]
#    objetos_directos(claves, "images/") -> ["images/b.jpg"]
def objetos_directos(claves, prefijo):
    return [clave for clave in claves if prefijo in clave]
