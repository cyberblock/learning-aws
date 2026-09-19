# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 3:18:56–3:35:57: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11936s
# Apunte: apuntes/08-serverless-lambda.md
#
# Ejercicios 08 · Serverless y AWS Lambda
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 08_serverless --mios


# 1. Tiempo de cálculo de una invocación en GB-segundo, que es la unidad con la que
#    Lambda factura la duración: (memoria en GB) × (duración en segundos).
#    1 GB = 1024 MB. gb_segundos(1000, 1024) -> 1.0
def gb_segundos(duracion_ms, memoria_mb):
    raise NotImplementedError("ejercicio 1")


# 2. ¿Es válida la configuración de una función? Límites de Lambda:
#    - memoria entre 128 y 10240 MB;
#    - tiempo de espera entre 1 y 900 segundos (15 minutos).
#    Devuelve True o False.
def configuracion_valida(memoria_mb, timeout_s):
    raise NotImplementedError("ejercicio 2")


# 3. Coste mensual del TIEMPO DE CÁLCULO. La capa gratuita cubre 400 000 GB-segundo al
#    mes; a partir de ahí, 0,0000166667 USD por GB-segundo.
#    coste_computo(400_000) -> 0.0
#    Redondea a 6 decimales.
def coste_computo(gb_seg_del_mes):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Coste mensual de las SOLICITUDES: el primer millón al mes es
#    gratuito y después se pagan 0,20 USD por cada millón de solicitudes.
#    coste_solicitudes(1_000_000) -> 0.0
#    coste_solicitudes(3_000_000) -> 0.4
#    Redondea a 6 decimales.
def coste_solicitudes(solicitudes):
    return round(solicitudes * 0.20, 6)
