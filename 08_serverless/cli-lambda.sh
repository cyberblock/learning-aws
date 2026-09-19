#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Lambda demo" 3:26:58: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12418s
# Apunte: apuntes/08-serverless-lambda.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea el rol de ejecución, despliega la función, la invoca y lee los registros.
set -euo pipefail
cd "$(dirname "$0")"

FUNCION=demo-lambda
ROL=demo-lambda-rol
REGION=us-east-1

# 1. Rol de ejecución: la consola lo crea sola; aquí se hace a mano.
#    La política de confianza dice QUIÉN puede asumirlo (el servicio Lambda).
aws iam create-role --role-name "$ROL" \
  --assume-role-policy-document file://politica-rol-lambda.json

#    La política gestionada básica solo permite escribir registros en CloudWatch
aws iam attach-role-policy --role-name "$ROL" \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

ROL_ARN=$(aws iam get-role --role-name "$ROL" --query Role.Arn --output text)
sleep 10   # IAM tarda unos segundos en propagar el rol nuevo

# 2. El código va en un zip
zip -q funcion.zip funcion_lambda.py

aws lambda create-function --region "$REGION" \
  --function-name "$FUNCION" \
  --runtime python3.13 \
  --role "$ROL_ARN" \
  --handler funcion_lambda.lambda_handler \
  --zip-file fileb://funcion.zip \
  --timeout 10 --memory-size 128

# 3. Invocar con un evento de prueba (como el botón "Probar" de la consola)
aws lambda invoke --region "$REGION" --function-name "$FUNCION" \
  --payload '{"nombre":"Joan"}' --cli-binary-format raw-in-base64-out respuesta-lambda.json
cat respuesta-lambda.json

# 4. Actualizar el código tras cambiarlo (el "Deploy" de la consola)
# zip -q funcion.zip funcion_lambda.py
# aws lambda update-function-code --function-name "$FUNCION" --zip-file fileb://funcion.zip --region "$REGION"

# 5. Los registros van a CloudWatch Logs, al grupo /aws/lambda/<función>
aws logs describe-log-streams --region "$REGION" \
  --log-group-name "/aws/lambda/${FUNCION}" \
  --order-by LastEventTime --descending --max-items 1

# Limpieza:
# aws lambda delete-function --function-name "$FUNCION" --region "$REGION"
# aws logs delete-log-group --log-group-name "/aws/lambda/${FUNCION}" --region "$REGION"
# aws iam detach-role-policy --role-name "$ROL" --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
# aws iam delete-role --role-name "$ROL"
