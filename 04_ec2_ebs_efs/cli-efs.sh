#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "EFS" 1:41:12: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6072s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Equivalente con la AWS CLI de lo que en el vídeo solo se explica con diapositivas.
# Crea un sistema de archivos EFS, un punto de montaje por subred y la regla de ciclo
# de vida que mueve a EFS-IA lo que no se toca en 60 días.
# ⚠️ EFS se paga por uso y es más caro que EBS. Bórralo al terminar.
set -euo pipefail

SUBRED=${1:?uso: ./cli-efs.sh subnet-0123456789abcdef0 sg-0123456789abcdef0}
GRUPO_SEG=${2:?falta el grupo de seguridad}
REGION=us-east-1

FS=$(aws efs create-file-system --region "$REGION" \
  --creation-token curso-aws-demo \
  --performance-mode generalPurpose \
  --tags Key=Name,Value=curso-aws-demo \
  --query FileSystemId --output text)

# Un punto de montaje por zona de disponibilidad: por eso EFS sirve a varias zonas a la vez
aws efs create-mount-target --file-system-id "$FS" \
  --subnet-id "$SUBRED" --security-groups "$GRUPO_SEG" --region "$REGION"

# Ciclo de vida: a IA tras 60 días sin accesos y de vuelta a estándar al primer acceso
aws efs put-lifecycle-configuration --file-system-id "$FS" --region "$REGION" \
  --lifecycle-policies '[{"TransitionToIA":"AFTER_60_DAYS"},{"TransitionToPrimaryStorageClass":"AFTER_1_ACCESS"}]'

aws efs describe-file-systems --file-system-id "$FS" --region "$REGION" \
  --query 'FileSystems[].{Id:FileSystemId,Tamano:SizeInBytes.Value,Estado:LifeCycleState}' --output table

# En la instancia Linux (paquete amazon-efs-utils):
# sudo mount -t efs -o tls "$FS":/ /mnt/datos

# Limpieza (primero los puntos de montaje, luego el sistema de archivos):
# aws efs delete-mount-target --mount-target-id fsmt-0123456789abcdef0 --region "$REGION"
# aws efs delete-file-system --file-system-id "$FS" --region "$REGION"
