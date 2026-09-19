#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "RDS demo" 2:56:10: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=10570s
# Apunte: apuntes/07-bases-de-datos.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea una instancia MySQL de la capa gratuita, sin acceso público, y una instantánea.
# ⚠️ Una base de datos RDS es de lo que más gasto genera si se olvida encendida.
set -euo pipefail

BD=demo-mysql
REGION=us-east-1
# La contraseña NO se escribe en el script: se pide al ejecutarlo
read -r -s -p "Contraseña del usuario maestro: " PASSWORD; echo

aws rds create-db-instance --region "$REGION" \
  --db-instance-identifier "$BD" \
  --engine mysql \
  --db-instance-class db.t4g.micro \
  --allocated-storage 20 --storage-type gp2 \
  --max-allocated-storage 1000 \
  --master-username admin --master-user-password "$PASSWORD" \
  --port 3306 \
  --backup-retention-period 7 \
  --no-publicly-accessible

aws rds wait db-instance-available --db-instance-identifier "$BD" --region "$REGION"

# El punto de enlace y el puerto son los datos de conexión de la aplicación
aws rds describe-db-instances --db-instance-identifier "$BD" --region "$REGION" \
  --query 'DBInstances[0].{Endpoint:Endpoint.Address,Puerto:Endpoint.Port,Motor:Engine,MultiAZ:MultiAZ}' \
  --output table

# Instantánea: sirve para copiarla a otra región o compartirla con otra cuenta
aws rds create-db-snapshot --region "$REGION" \
  --db-instance-identifier "$BD" --db-snapshot-identifier demo-snapshot

# A RDS no se entra por SSH: solo se conecta por el motor
# mysql -h <endpoint> -P 3306 -u admin -p

# Limpieza:
# aws rds delete-db-snapshot --db-snapshot-identifier demo-snapshot --region "$REGION"
# aws rds delete-db-instance --db-instance-identifier "$BD" --skip-final-snapshot --delete-automated-backups --region "$REGION"
