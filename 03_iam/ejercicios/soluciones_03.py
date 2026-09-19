# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 0:53:05–1:07:09: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s
# Apunte: apuntes/03-seguridad-iam.md
#
# Soluciones de los ejercicios 03 · Seguridad e IAM


def construir_politica(acciones):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": list(acciones),
                "Resource": "*",
            }
        ],
    }


def url_inicio_sesion(alias, id_cuenta=None):
    identificador = alias or id_cuenta
    if not identificador:
        raise ValueError("hace falta un alias o un ID de cuenta")
    return f"https://{identificador}.signin.aws.amazon.com/console"


def _como_lista(valor):
    return valor if isinstance(valor, list) else [valor]


def _coincide(patron, accion):
    if patron == "*":
        return True
    if patron.endswith("*"):
        return accion.startswith(patron[:-1])
    return patron == accion


def permite(politica, accion):
    for sentencia in politica["Statement"]:
        if sentencia.get("Effect") != "Allow":
            continue
        if any(_coincide(p, accion) for p in _como_lista(sentencia.get("Action", []))):
            return True
    return False


def es_administrador(politica):
    for sentencia in politica["Statement"]:
        if sentencia.get("Effect") != "Allow":
            continue
        acciones = _como_lista(sentencia.get("Action", []))
        recursos = _como_lista(sentencia.get("Resource", []))
        if "*" in acciones and "*" in recursos:
            return True
    return False
