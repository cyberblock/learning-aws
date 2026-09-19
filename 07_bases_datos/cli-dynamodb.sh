#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "DynamoDB demo" 3:13:12: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11592s
# Apunte: apuntes/07-bases-de-datos.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea una tabla con clave de partición numérica, mete dos elementos y los consulta.
set -euo pipefail
cd "$(dirname "$0")"

TABLA=demo-usuarios
REGION=us-east-1

# Solo se declaran los atributos de la clave: el resto del esquema es libre
aws dynamodb create-table --region "$REGION" \
  --table-name "$TABLA" \
  --attribute-definitions AttributeName=user_id,AttributeType=N \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

aws dynamodb wait table-exists --table-name "$TABLA" --region "$REGION"

aws dynamodb put-item --region "$REGION" --table-name "$TABLA" --item file://item-usuario.json

# Otro elemento con menos atributos: en una tabla NoSQL no pasa nada
aws dynamodb put-item --region "$REGION" --table-name "$TABLA" \
  --item '{"user_id":{"N":"1"},"nombre":{"S":"Stefan"}}'

aws dynamodb get-item --region "$REGION" --table-name "$TABLA" \
  --key '{"user_id":{"N":"1234"}}'

aws dynamodb scan --region "$REGION" --table-name "$TABLA" \
  --query 'Items[].{Id:user_id.N,Nombre:nombre.S}' --output table

# Limpieza:
# aws dynamodb delete-table --table-name "$TABLA" --region "$REGION"
