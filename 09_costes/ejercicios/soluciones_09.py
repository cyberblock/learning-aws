# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 3:35:57–3:50:13: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12957s
# Apunte: apuntes/09-costes-facturacion.md
#
# Soluciones de los ejercicios 09 · Costes y facturación

from collections import defaultdict


def coste_por_servicio(filas):
    totales = defaultdict(float)
    for fila in filas:
        totales[fila["servicio"]] += float(fila["coste_usd"])
    return {servicio: round(total, 2) for servicio, total in totales.items()}


def top_servicios(costes, n):
    ordenados = sorted(costes.items(), key=lambda par: (-par[1], par[0]))
    return ordenados[:n]


def prevision_fin_de_mes(gasto_acumulado, dias_transcurridos, dias_del_mes):
    if dias_transcurridos == 0:
        raise ValueError("hacen falta días transcurridos para estimar el gasto")
    return round(gasto_acumulado / dias_transcurridos * dias_del_mes, 2)


def etiquetas_de_usuario(etiquetas):
    nombres = set()
    for etiqueta in etiquetas:
        if not etiqueta.startswith("user:"):
            continue
        nombres.add(etiqueta[len("user:"):].split("$")[0])
    return sorted(nombres)
