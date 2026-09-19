#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Dashboard facturación" 3:36:33: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12993s
# Apunte: apuntes/09-costes-facturacion.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Consulta el gasto por servicio y por etiqueta, la previsión del mes y etiqueta recursos.
# Solo consulta y etiquetado: no crea recursos que cuesten dinero.
set -euo pipefail

DESDE=$(date -u +%Y-%m-01)
HASTA=$(date -u +%Y-%m-%d)
FIN_MES=$(date -u -d "$(date -u +%Y-%m-01) +1 month" +%Y-%m-01)

# Gasto de este mes agrupado por servicio (lo que muestra el panel de facturación)
aws ce get-cost-and-usage \
  --time-period Start="$DESDE",End="$HASTA" \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[].{Servicio:Keys[0],Coste:Metrics.UnblendedCost.Amount}' \
  --output table

# Lo mismo, pero agrupado por una etiqueta de asignación de costes
aws ce get-cost-and-usage \
  --time-period Start="$DESDE",End="$HASTA" \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=TAG,Key=department

# Previsión hasta fin de mes a partir del histórico
aws ce get-cost-forecast \
  --time-period Start="$HASTA",End="$FIN_MES" \
  --metric UNBLENDED_COST --granularity MONTHLY

# Etiquetas de asignación de costes: hay que ACTIVARLAS para que aparezcan en los informes
aws ce list-cost-allocation-tags --status Inactive --max-results 25
# aws ce update-cost-allocation-tags-status --cost-allocation-tags-status TagKey=department,Status=Active

# Etiquetar recursos y buscarlos luego por etiqueta (lo que hace el editor de etiquetas)
# aws resourcegroupstaggingapi tag-resources \
#   --resource-arn-list arn:aws:ec2:us-east-1:123456789012:security-group/sg-0123456789abcdef0 \
#   --tags department=IT
aws resourcegroupstaggingapi get-resources --tag-filters Key=department,Values=IT

# Un grupo de recursos reúne todo lo que comparte etiqueta
# aws resource-groups create-group --name department-IT \
#   --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"department\",\"Values\":[\"IT\"]}]}"}'
