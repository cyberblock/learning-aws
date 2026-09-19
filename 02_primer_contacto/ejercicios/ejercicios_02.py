# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:34:12–0:53:05: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s
# Apunte: apuntes/02-primer-contacto-aws.md
#
# Ejercicios 02 · Primer contacto con AWS (presupuestos)
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 02_primer_contacto --mios


# 1. ¿A cuántos dólares corresponde un umbral en porcentaje?
#    umbral_en_dolares(10, 50) -> 5.0   (el ejemplo del vídeo: 50 % de 10 USD)
#    Redondea a 2 decimales.
def umbral_en_dolares(limite_usd, porcentaje):
    raise NotImplementedError("ejercicio 1")


# 2. Construye el dict del presupuesto que espera `aws budgets create-budget --budget`:
#    presupuesto de COSTE, MENSUAL, con el límite en USD.
#    Ojo: la API espera el importe como texto ("10"), no como número.
#    Mira 02_primer_contacto/presupuesto.json si te atascas.
def construir_presupuesto(nombre, limite_usd):
    raise NotImplementedError("ejercicio 2")


# 3. Construye UNA notificación con suscriptor para --notifications-with-subscribers:
#    alerta por gasto REAL ("ACTUAL") mayor que `porcentaje` % del presupuesto,
#    enviada por correo a `correo`.
def construir_notificacion(correo, porcentaje):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Devuelve, ordenados de menor a mayor, los umbrales (en %) que ya han
#    saltado. Un umbral salta cuando el gasto ALCANZA o supera ese porcentaje del límite.
#    alertas_disparadas(5, 10, [80, 50, 100]) -> [50]
def alertas_disparadas(gasto_usd, limite_usd, umbrales):
    disparadas = []
    for umbral in umbrales:
        if gasto_usd > umbral:
            disparadas.append(umbral)
    return disparadas
