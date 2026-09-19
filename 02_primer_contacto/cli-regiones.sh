#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Tour consola AWS" 0:45:22: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2722s
# Apunte: apuntes/02-primer-contacto-aws.md
#
# Equivalente con la AWS CLI del tour por las regiones. NO aparece en el vídeo.
# Solo consulta información: no crea nada ni tiene coste.
set -euo pipefail

# ¿Con qué identidad y en qué región está trabajando la CLI?
aws sts get-caller-identity
aws configure get region || echo "Sin región por defecto: usa --region o 'aws configure'"

# Regiones habilitadas en la cuenta
aws ec2 describe-regions --query 'Regions[].RegionName' --output text

# Zonas de disponibilidad de Norte de Virginia
aws ec2 describe-availability-zones \
  --region us-east-1 \
  --query 'AvailabilityZones[].[ZoneName,ZoneId,State]' \
  --output table
