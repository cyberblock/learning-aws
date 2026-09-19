#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Qué es IAM" 0:53:36: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3216s
# Apunte: apuntes/03-seguridad-iam.md
#
# Equivalente con la AWS CLI del documento JSON que se explica en el vídeo. NO aparece en el vídeo.
# Crea una política de solo lectura (EC2, ELB y CloudWatch) y la adjunta a un grupo.
set -euo pipefail
cd "$(dirname "$0")"

GRUPO=solo-lectura
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ARN="arn:aws:iam::${ACCOUNT_ID}:policy/consulta-ec2-elb-cloudwatch"

aws iam create-policy \
  --policy-name consulta-ec2-elb-cloudwatch \
  --policy-document file://politica-solo-lectura.json \
  --description "Solo lectura de EC2, ELB y CloudWatch (mínimo privilegio)"

aws iam create-group --group-name "$GRUPO"
aws iam attach-group-policy --group-name "$GRUPO" --policy-arn "$ARN"

# Qué políticas tiene el grupo
aws iam list-attached-group-policies --group-name "$GRUPO" --output table

# Limpieza:
# aws iam detach-group-policy --group-name "$GRUPO" --policy-arn "$ARN"
# aws iam delete-group --group-name "$GRUPO"
# aws iam delete-policy --policy-arn "$ARN"
