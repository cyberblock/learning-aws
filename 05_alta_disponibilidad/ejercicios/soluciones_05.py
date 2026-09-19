# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 1:47:33–2:27:32: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s
# Apunte: apuntes/05-alta-disponibilidad.md
#
# Soluciones de los ejercicios 05 · Alta disponibilidad, balanceadores y autoescalado


def tipo_de_escalado(antes, despues):
    cambia_tipo = antes["tipo"] != despues["tipo"]
    cambia_numero = antes["instancias"] != despues["instancias"]
    if cambia_tipo and cambia_numero:
        return "mixto"
    if cambia_tipo:
        return "vertical"
    if cambia_numero:
        return "horizontal"
    return "ninguno"


def capacidad_objetivo(deseada, minimo, maximo, delta):
    return max(minimo, min(maximo, deseada + delta))


def reparto(destinos, peticiones):
    sanos = [d["id"] for d in destinos if d.get("estado") == "healthy"]
    if not sanos:
        return []
    return [sanos[i % len(sanos)] for i in range(peticiones)]


def es_alta_disponibilidad(instancias):
    zonas = {i["az"] for i in instancias if i.get("estado") == "healthy"}
    return len(zonas) >= 2
