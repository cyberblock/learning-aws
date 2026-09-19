#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "S3 demo" 2:35:38: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9338s
# Apunte: apuntes/06-s3.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea un bucket bloqueado al público, sube objetos y genera una URL prefirmada.
# ⚠️ El nombre del bucket es ÚNICO EN TODO AWS: cambia BUCKET antes de ejecutarlo.
set -euo pipefail

BUCKET=mi-bucket-unico-del-curso
REGION=us-east-1

aws s3 mb "s3://${BUCKET}" --region "$REGION"

# Bloquear todo acceso público (es el valor por defecto desde 2023; se deja explícito)
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Versionado: guarda cada versión del objeto y permite volver atrás
aws s3api put-bucket-versioning --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

# Subir objetos. La "carpeta" images/ es solo un prefijo de la clave
echo "hola" > mi-archivo.txt
aws s3 cp mi-archivo.txt "s3://${BUCKET}/mi-archivo.txt"
aws s3 cp mi-archivo.txt "s3://${BUCKET}/images/otra-copia.txt"
aws s3 ls "s3://${BUCKET}" --recursive

# La URL pública da AccessDenied con el bucket bloqueado; esta funciona 1 hora
aws s3 presign "s3://${BUCKET}/mi-archivo.txt" --expires-in 3600

# Versiones de un objeto (con el versionado activo)
aws s3api list-object-versions --bucket "$BUCKET" --prefix mi-archivo.txt \
  --query 'Versions[].{Version:VersionId,Ultima:IsLatest,Fecha:LastModified}' --output table

# Para servir contenido al público de verdad se usa una política de bucket:
# aws s3api put-bucket-policy --bucket "$BUCKET" --policy file://politica-bucket-lectura-publica.json

# Limpieza (con versionado hay que vaciar también las versiones antiguas):
# aws s3 rm "s3://${BUCKET}" --recursive
# aws s3 rb "s3://${BUCKET}"
