# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:34:12–0:53:05: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s
# Apunte: apuntes/02-primer-contacto-aws.md
#
# Soluciones 02 · Primer contacto con AWS (presupuestos)


# 1.
def umbral_en_dolares(limite_usd, porcentaje):
    return round(limite_usd * porcentaje / 100, 2)


# 2.
def construir_presupuesto(nombre, limite_usd):
    return {
        "BudgetName": nombre,
        "BudgetLimit": {"Amount": str(limite_usd), "Unit": "USD"},
        "TimeUnit": "MONTHLY",
        "BudgetType": "COST",
    }


# 3.
def construir_notificacion(correo, porcentaje):
    return {
        "Notification": {
            "NotificationType": "ACTUAL",
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": porcentaje,
            "ThresholdType": "PERCENTAGE",
        },
        "Subscribers": [{"SubscriptionType": "EMAIL", "Address": correo}],
    }


# 4. Fallos de la versión original:
#    - comparaba el gasto en dólares con el umbral en porcentaje
#    - usaba > en lugar de >= (al llegar justo al umbral no saltaba)
#    - no ordenaba el resultado
def alertas_disparadas(gasto_usd, limite_usd, umbrales):
    porcentaje_gastado = gasto_usd / limite_usd * 100
    return sorted(u for u in umbrales if porcentaje_gastado >= u)
