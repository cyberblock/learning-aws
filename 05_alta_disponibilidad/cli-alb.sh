#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "ALB demo" 2:02:42: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=7362s
# Apunte: apuntes/05-alta-disponibilidad.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea un Application Load Balancer con su grupo de destino y registra dos instancias.
# ⚠️ Un ALB cuesta dinero por hora, esté o no recibiendo tráfico. Limpia al terminar.
set -euo pipefail

INSTANCIA_1=${1:?uso: ./cli-alb.sh i-aaa i-bbb}
INSTANCIA_2=${2:?falta la segunda instancia}
REGION=us-east-1

VPC=$(aws ec2 describe-vpcs --region "$REGION" \
  --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)

# Un ALB necesita subredes de AL MENOS DOS zonas de disponibilidad
SUBREDES=$(aws ec2 describe-subnets --region "$REGION" \
  --filters Name=vpc-id,Values="$VPC" --query 'Subnets[].SubnetId' --output text)

GRUPO_ID=$(aws ec2 create-security-group --region "$REGION" \
  --group-name demo-sg-alb --description "Permite HTTP al ALB" \
  --vpc-id "$VPC" --query GroupId --output text)

aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$GRUPO_ID" \
  --ip-permissions 'IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges=[{CidrIp=0.0.0.0/0}]'

# Grupo de destino: a quién manda el tráfico y cómo comprueba que sigue vivo
DESTINO=$(aws elbv2 create-target-group --region "$REGION" \
  --name demo-tg-alb --protocol HTTP --port 80 --vpc-id "$VPC" \
  --target-type instance --health-check-path / \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 register-targets --region "$REGION" --target-group-arn "$DESTINO" \
  --targets Id="$INSTANCIA_1" Id="$INSTANCIA_2"

ALB=$(aws elbv2 create-load-balancer --region "$REGION" \
  --name demo-alb --type application --scheme internet-facing \
  --subnets $SUBREDES --security-groups "$GRUPO_ID" \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# Agente de escucha: puerto 80 hacia el grupo de destino
aws elbv2 create-listener --region "$REGION" --load-balancer-arn "$ALB" \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn="$DESTINO"

DNS=$(aws elbv2 describe-load-balancers --region "$REGION" --load-balancer-arns "$ALB" \
  --query 'LoadBalancers[0].DNSName' --output text)
echo "Recarga varias veces http://${DNS} : las respuestas alternan entre instancias"

# Estado de salud de cada destino (unhealthy = el ALB deja de mandarle tráfico)
aws elbv2 describe-target-health --region "$REGION" --target-group-arn "$DESTINO" \
  --query 'TargetHealthDescriptions[].{Instancia:Target.Id,Estado:TargetHealth.State}' --output table

# Limpieza (en este orden):
# aws elbv2 delete-load-balancer --load-balancer-arn "$ALB" --region "$REGION"
# aws elbv2 delete-target-group --target-group-arn "$DESTINO" --region "$REGION"
# aws ec2 delete-security-group --group-id "$GRUPO_ID" --region "$REGION"
