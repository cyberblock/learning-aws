#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "EC2 demo" 1:13:27: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4407s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Lanza una instancia t2.micro con Amazon Linux, Apache y el puerto 80 abierto.
# ⚠️ Crea recursos reales. Ejecuta la limpieza del final cuando termines.
set -euo pipefail
cd "$(dirname "$0")"

CLAVES=demo-par-claves
GRUPO=demo-web
REGION=us-east-1

# AMI de Amazon Linux 2023 más reciente de la región (evita copiar IDs a mano)
AMI=$(aws ssm get-parameter \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --region "$REGION" --query Parameter.Value --output text)

# 1. Par de claves. La clave privada solo se descarga aquí: guárdala bien.
aws ec2 create-key-pair --key-name "$CLAVES" --key-type rsa --key-format pem \
  --region "$REGION" --query KeyMaterial --output text > "${CLAVES}.pem"
chmod 400 "${CLAVES}.pem"

# 2. Grupo de seguridad (el cortafuegos): SSH y HTTP desde internet
GRUPO_ID=$(aws ec2 create-security-group --group-name "$GRUPO" \
  --description "Demo del curso: SSH y HTTP" \
  --region "$REGION" --query GroupId --output text)

aws ec2 authorize-security-group-ingress --group-id "$GRUPO_ID" --region "$REGION" \
  --ip-permissions 'IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges=[{CidrIp=0.0.0.0/0}]' \
                   'IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges=[{CidrIp=0.0.0.0/0}]'

# 3. La instancia, con el script de arranque
INSTANCIA=$(aws ec2 run-instances --region "$REGION" \
  --image-id "$AMI" \
  --instance-type t2.micro \
  --key-name "$CLAVES" \
  --security-group-ids "$GRUPO_ID" \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=mi-primera-instancia}]' \
  --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids "$INSTANCIA" --region "$REGION"

IP=$(aws ec2 describe-instances --instance-ids "$INSTANCIA" --region "$REGION" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Abre http://${IP}   (http, NO https: solo está abierto el puerto 80)"
echo "SSH: ssh -i ${CLAVES}.pem ec2-user@${IP}"

# Parar y volver a arrancar: la IP pública CAMBIA (salvo con una IP elástica)
# aws ec2 stop-instances  --instance-ids "$INSTANCIA" --region "$REGION"
# aws ec2 start-instances --instance-ids "$INSTANCIA" --region "$REGION"

# Limpieza:
# aws ec2 terminate-instances --instance-ids "$INSTANCIA" --region "$REGION"
# aws ec2 wait instance-terminated --instance-ids "$INSTANCIA" --region "$REGION"
# aws ec2 delete-security-group --group-id "$GRUPO_ID" --region "$REGION"
# aws ec2 delete-key-pair --key-name "$CLAVES" --region "$REGION"
