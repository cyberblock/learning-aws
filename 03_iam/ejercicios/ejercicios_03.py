# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:53:05–1:07:09: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s
# Apunte: apuntes/03-seguridad-iam.md
#
# Ejercicios 03 · Seguridad e IAM (políticas, grupos y acceso)
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 03_iam --mios


# 1. Construye el documento JSON (como dict) de una política que PERMITE las acciones
#    indicadas sobre todos los recursos.
#    construir_politica(["ec2:DescribeInstances"]) ->
#        {"Version": "2012-10-17",
#         "Statement": [{"Effect": "Allow", "Action": ["ec2:DescribeInstances"], "Resource": "*"}]}
#    La versión siempre es "2012-10-17" (es la fecha del lenguaje de políticas, no la de hoy).
def construir_politica(acciones):
    raise NotImplementedError("ejercicio 1")


# 2. URL de inicio de sesión de los usuarios IAM de la cuenta a partir del alias.
#    url_inicio_sesion("joan-aws") -> "https://joan-aws.signin.aws.amazon.com/console"
#    Si el alias es None o está vacío, usa el ID de cuenta de 12 dígitos que te pasen
#    como segundo argumento: url_inicio_sesion("", "123456789012") ->
#        "https://123456789012.signin.aws.amazon.com/console"
def url_inicio_sesion(alias, id_cuenta=None):
    raise NotImplementedError("ejercicio 2")


# 3. ¿La política permite esta acción? Ten en cuenta el comodín final de las acciones:
#    "ec2:Describe*" permite "ec2:DescribeInstances", pero no "ec2:RunInstances".
#    Una acción "*" (a secas) lo permite todo. Solo miramos sentencias con Effect "Allow".
#    permite(politica, "ec2:DescribeInstances") -> True
def permite(politica, accion):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Debe decir si una política es de administrador, es decir, si
#    ALGUNA sentencia permite TODAS las acciones ("*") sobre TODOS los recursos ("*").
#    Pistas: `Action` y `Resource` pueden ser un texto o una lista, y una sentencia con
#    Effect "Deny" nunca concede permisos.
def es_administrador(politica):
    for sentencia in politica["Statement"]:
        if sentencia["Action"] == "*" or sentencia["Resource"] == "*":
            return True
    return False
