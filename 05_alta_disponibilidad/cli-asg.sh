#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Auto Scaling demo" 2:16:11: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8171s
# Apunte: apuntes/05-alta-disponibilidad.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Plantilla de lanzamiento + grupo de autoescalado (mín 1, deseada 2, máx 4) conectado
# al grupo de destino del ALB, con comprobaciones de estado del balanceador.
# ⚠️ Crea instancias reales. Borra PRIMERO el grupo de autoescalado: si terminas las
# instancias antes, el grupo las vuelve a lanzar.
set -euo pipefail
cd "$(dirname "$0")"

DESTINO_ARN=${1:?uso: ./cli-asg.sh arn:aws:elasticloadbalancing:...:targetgroup/demo-tg-alb/...}
REGION=us-east-1

AMI=$(aws ssm get-parameter --region "$REGION" \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query Parameter.Value --output text)

VPC=$(aws ec2 describe-vpcs --region "$REGION" \
  --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
SUBREDES=$(aws ec2 describe-subnets --region "$REGION" \
  --filters Name=vpc-id,Values="$VPC" --query 'Subnets[].SubnetId' --output text | tr '\t' ',')
GRUPO_ID=$(aws ec2 describe-security-groups --region "$REGION" \
  --filters Name=group-name,Values=demo-sg-alb --query 'SecurityGroups[0].GroupId' --output text)

# El script de arranque va dentro de la plantilla, codificado en base64
USER_DATA=$(base64 -w0 ../04_ec2_ebs_efs/user-data.sh)

aws ec2 create-launch-template --region "$REGION" \
  --launch-template-name demo-template-launch \
  --version-description "v1 del curso" \
  --launch-template-data "{\"ImageId\":\"$AMI\",\"InstanceType\":\"t3.micro\",\"SecurityGroupIds\":[\"$GRUPO_ID\"],\"UserData\":\"$USER_DATA\"}"

aws autoscaling create-auto-scaling-group --region "$REGION" \
  --auto-scaling-group-name demo-asg \
  --launch-template LaunchTemplateName=demo-template-launch,Version='$Latest' \
  --min-size 1 --desired-capacity 2 --max-size 4 \
  --vpc-zone-identifier "$SUBREDES" \
  --target-group-arns "$DESTINO_ARN" \
  --health-check-type ELB --health-check-grace-period 120

# Política de escalado: mantener la CPU media al 50 % (en el vídeo se deja "sin política")
aws autoscaling put-scaling-policy --region "$REGION" \
  --auto-scaling-group-name demo-asg \
  --policy-name cpu-al-50 --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"TargetValue":50.0,"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"}}'

aws autoscaling describe-auto-scaling-groups --region "$REGION" \
  --auto-scaling-group-names demo-asg \
  --query 'AutoScalingGroups[0].{Min:MinSize,Deseada:DesiredCapacity,Max:MaxSize,Instancias:length(Instances)}' \
  --output table

# Limpieza (el orden importa):
# aws autoscaling delete-auto-scaling-group --auto-scaling-group-name demo-asg --force-delete --region "$REGION"
# aws ec2 delete-launch-template --launch-template-name demo-template-launch --region "$REGION"
