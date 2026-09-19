# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 3:35:57–3:50:13: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12957s
# Apunte: apuntes/09-costes-facturacion.md
#
# Ejercicios 09 · Costes y facturación
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 09_costes --mios
#
# Las filas de coste son dicts como los del informe de uso (09_costes/costes-ejemplo.csv):
#   {"fecha": "2026-04-01", "servicio": "Amazon EC2",
#    "etiqueta": "user:department$IT", "coste_usd": "3.20"}


# 1. Suma el coste de cada servicio. Devuelve un dict {servicio: coste} con el coste
#    redondeado a 2 decimales.
def coste_por_servicio(filas):
    raise NotImplementedError("ejercicio 1")


# 2. Los `n` servicios que más gastan, de mayor a menor, como lista de tuplas
#    (servicio, coste). Si dos gastan lo mismo, ordénalos por nombre.
#    top_servicios({"Amazon EC2": 10.6, "Amazon S3": 0.35}, 1) -> [("Amazon EC2", 10.6)]
def top_servicios(costes, n):
    raise NotImplementedError("ejercicio 2")


# 3. Previsión de gasto a fin de mes con el ritmo actual:
#    (gasto acumulado / días transcurridos) × días del mes. Redondea a 2 decimales.
#    prevision_fin_de_mes(15.4, 4, 30) -> 115.5
#    Si `dias_transcurridos` es 0, lanza ValueError.
def prevision_fin_de_mes(gasto_acumulado, dias_transcurridos, dias_del_mes):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Devuelve solo las etiquetas DEFINIDAS POR EL USUARIO, que son
#    las que empiezan por "user:"; las generadas por AWS empiezan por "aws:". El
#    resultado son los nombres de etiqueta sin el prefijo, sin repetir y ordenados.
#    etiquetas_de_usuario(["user:department$IT", "aws:createdBy$IAMUser"]) -> ["department"]
def etiquetas_de_usuario(etiquetas):
    return sorted(etiqueta.split("$")[0] for etiqueta in etiquetas)
