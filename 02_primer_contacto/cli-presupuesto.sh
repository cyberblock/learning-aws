#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Presupuesto AWS" 0:41:24: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2484s
# Apunte: apuntes/02-primer-contacto-aws.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea un presupuesto de 10 USD/mes con alerta por correo al 50 %.
# Antes de ejecutarlo, cambia la dirección de correo de notificaciones.json.
set -euo pipefail
cd "$(dirname "$0")"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws budgets create-budget \
  --account-id "$ACCOUNT_ID" \
  --budget file://presupuesto.json \
  --notifications-with-subscribers file://notificaciones.json

aws budgets describe-budgets \
  --account-id "$ACCOUNT_ID" \
  --query 'Budgets[].{Nombre:BudgetName,Limite:BudgetLimit.Amount,Periodo:TimeUnit}' \
  --output table

# Limpieza (el presupuesto no cuesta nada; bórralo solo si ya no lo quieres):
# aws budgets delete-budget --account-id "$ACCOUNT_ID" --budget-name presupuesto-mensual
