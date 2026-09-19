#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "EBS demo" 1:35:20: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=5720s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea un volumen EBS de 2 GiB en la MISMA zona que la instancia y lo adjunta.
# ⚠️ Crea recursos reales. Ejecuta la limpieza del final cuando termines.
set -euo pipefail

INSTANCIA=${1:?uso: ./cli-volumen-ebs.sh i-0123456789abcdef0}
REGION=us-east-1

# El volumen vive en UNA zona de disponibilidad: la de la instancia
ZONA=$(aws ec2 describe-instances --instance-ids "$INSTANCIA" --region "$REGION" \
  --query 'Reservations[0].Instances[0].Placement.AvailabilityZone' --output text)

VOLUMEN=$(aws ec2 create-volume --region "$REGION" \
  --availability-zone "$ZONA" --size 2 --volume-type gp3 \
  --query VolumeId --output text)

aws ec2 wait volume-available --volume-ids "$VOLUMEN" --region "$REGION"
aws ec2 attach-volume --volume-id "$VOLUMEN" --instance-id "$INSTANCIA" \
  --device /dev/sdf --region "$REGION"

# Los dos volúmenes de la instancia y su "borrar al terminar"
aws ec2 describe-instances --instance-ids "$INSTANCIA" --region "$REGION" \
  --query 'Reservations[0].Instances[0].BlockDeviceMappings[].{Disp:DeviceName,Borrar:Ebs.DeleteOnTermination}' \
  --output table

# Conservar el volumen raíz al terminar la instancia (por defecto se borra)
aws ec2 modify-instance-attribute --instance-id "$INSTANCIA" --region "$REGION" \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"DeleteOnTermination":false}}]'

# Mover datos a otra zona de disponibilidad: instantánea y restaurar allí
# aws ec2 create-snapshot --volume-id "$VOLUMEN" --description "copia del volumen de datos" --region "$REGION"

# Limpieza:
# aws ec2 detach-volume --volume-id "$VOLUMEN" --region "$REGION"
# aws ec2 wait volume-available --volume-ids "$VOLUMEN" --region "$REGION"
# aws ec2 delete-volume --volume-id "$VOLUMEN" --region "$REGION"
