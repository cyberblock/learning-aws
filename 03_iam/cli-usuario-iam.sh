#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Primer usuario IAM" 0:57:44: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3464s
# Apunte: apuntes/03-seguridad-iam.md
#
# Equivalente con la AWS CLI de la demo de consola. NO aparece en el vídeo.
# Crea el grupo admin, le adjunta AdministratorAccess, crea un usuario IAM con
# contraseña de un solo uso y lo mete en el grupo. Ejecútalo con el usuario root
# (o con otro usuario que tenga permisos de IAM).
set -euo pipefail
cd "$(dirname "$0")"

GRUPO=admin
USUARIO=joan
ALIAS=mi-cuenta-aws          # cámbialo: el alias es único en todo AWS

# 1. Grupo + política gestionada por AWS (permiso total; en producción, mínimo privilegio)
aws iam create-group --group-name "$GRUPO"
aws iam attach-group-policy \
  --group-name "$GRUPO" \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# 2. Usuario con acceso a la consola y cambio de contraseña en el primer inicio de sesión
aws iam create-user --user-name "$USUARIO"
aws iam create-login-profile \
  --user-name "$USUARIO" \
  --password "$(openssl rand -base64 18)" \
  --password-reset-required

# 3. El usuario hereda los permisos del grupo
aws iam add-user-to-group --user-name "$USUARIO" --group-name "$GRUPO"

# 4. Alias de cuenta: URL de acceso legible en lugar de los 12 dígitos del ID
aws iam create-account-alias --account-alias "$ALIAS"
echo "Entra en: https://${ALIAS}.signin.aws.amazon.com/console"

aws iam list-users --query 'Users[].UserName' --output table

# Limpieza (en este orden; si no, IAM se queja de que el usuario aún tiene dependencias):
# aws iam remove-user-from-group --user-name "$USUARIO" --group-name "$GRUPO"
# aws iam delete-login-profile --user-name "$USUARIO"
# aws iam delete-user --user-name "$USUARIO"
# aws iam detach-group-policy --group-name "$GRUPO" --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
# aws iam delete-group --group-name "$GRUPO"
# aws iam delete-account-alias --account-alias "$ALIAS"
