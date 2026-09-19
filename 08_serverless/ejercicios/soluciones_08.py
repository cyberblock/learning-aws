# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 3:18:56–3:35:57: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11936s
# Apunte: apuntes/08-serverless-lambda.md
#
# Soluciones de los ejercicios 08 · Serverless y AWS Lambda

GB_SEG_GRATIS = 400_000
PRECIO_GB_SEG = 0.0000166667
SOLICITUDES_GRATIS = 1_000_000
PRECIO_POR_MILLON = 0.20


def gb_segundos(duracion_ms, memoria_mb):
    return (memoria_mb / 1024) * (duracion_ms / 1000)


def configuracion_valida(memoria_mb, timeout_s):
    return 128 <= memoria_mb <= 10240 and 1 <= timeout_s <= 900


def coste_computo(gb_seg_del_mes):
    facturables = max(0, gb_seg_del_mes - GB_SEG_GRATIS)
    return round(facturables * PRECIO_GB_SEG, 6)


def coste_solicitudes(solicitudes):
    facturables = max(0, solicitudes - SOLICITUDES_GRATIS)
    return round(facturables / 1_000_000 * PRECIO_POR_MILLON, 6)
