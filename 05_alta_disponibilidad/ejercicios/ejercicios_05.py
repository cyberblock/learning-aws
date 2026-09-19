# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 1:47:33–2:27:32: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s
# Apunte: apuntes/05-alta-disponibilidad.md
#
# Ejercicios 05 · Alta disponibilidad, balanceadores y autoescalado
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 05_alta_disponibilidad --mios


# 1. ¿Qué tipo de escalado se ha hecho? Los estados son dicts:
#       {"tipo": "t2.micro", "instancias": 1}
#    - cambia el tipo de instancia y no el número  -> "vertical"
#    - cambia el número y no el tipo               -> "horizontal"
#    - no cambia nada                              -> "ninguno"
#    - cambian los dos                             -> "mixto"
def tipo_de_escalado(antes, despues):
    raise NotImplementedError("ejercicio 1")


# 2. Capacidad que acaba teniendo un grupo de autoescalado al pedirle `delta` instancias
#    (positivo o negativo). Nunca baja del mínimo ni sube del máximo.
#    capacidad_objetivo(deseada=2, minimo=1, maximo=4, delta=5) -> 4
def capacidad_objetivo(deseada, minimo, maximo, delta):
    raise NotImplementedError("ejercicio 2")


# 3. Reparto por turnos (round robin) del balanceador: devuelve, para `peticiones`
#    peticiones seguidas, el id del destino que responde a cada una. Solo entran los
#    destinos "healthy"; si no hay ninguno, devuelve una lista vacía.
#    destinos = [{"id": "i-a", "estado": "healthy"}, {"id": "i-b", "estado": "unhealthy"}]
#    reparto(destinos, 3) -> ["i-a", "i-a", "i-a"]
def reparto(destinos, peticiones):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Debe decir si un despliegue tiene alta disponibilidad, es decir,
#    si hay instancias SANAS en AL MENOS DOS zonas de disponibilidad distintas.
#    instancias = [{"id": "i-a", "az": "us-east-1a", "estado": "healthy"},
#                  {"id": "i-b", "az": "us-east-1a", "estado": "healthy"}]  -> False
def es_alta_disponibilidad(instancias):
    if len(instancias) >= 2:
        return True
    return False
