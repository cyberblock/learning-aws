"""Comprueba, sin conectarse a AWS, los comandos `aws ...` de los scripts .sh.

Para cada comando se verifica con los modelos de botocore (los mismos que usa la AWS CLI)
que existen el servicio, la operación (o el waiter) y cada una de las opciones `--xxx`.
No detecta errores de valores (un ID inventado, por ejemplo), solo de sintaxis de la CLI.
"""

import re
from pathlib import Path

import botocore.session
import pytest
from botocore import xform_name

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = sorted(p for p in RAIZ.glob("[0-9][0-9]_*/**/*.sh"))

# Nombre en la CLI -> nombre del servicio en botocore
SERVICIOS = {"s3api": "s3"}

# Comandos de alto nivel de `aws s3` (personalizaciones de la CLI, no están en botocore)
S3_ALTO_NIVEL = {"cp", "mv", "rm", "ls", "mb", "rb", "sync", "presign", "website"}

# Opciones globales de la CLI y opciones añadidas por personalizaciones
OPCIONES_GLOBALES = {
    "query", "output", "region", "profile", "no-cli-pager", "cli-input-json",
    "generate-cli-skeleton", "debug", "endpoint-url", "no-paginate", "max-items",
    "page-size", "starting-token", "cli-binary-format",
}
PERSONALIZACIONES = {
    ("ec2", "run-instances"): {"count"},
    ("lambda", "create-function"): {"zip-file"},
    ("lambda", "update-function-code"): {"zip-file"},
}

sesion = botocore.session.get_session()


def comandos(texto):
    """Devuelve cada comando `aws ...` de un script (une las líneas partidas con \\)."""
    texto = re.sub(r"\\\r?\n", " ", texto)
    lineas = [l for l in texto.splitlines() if not l.lstrip().startswith("#")]
    for linea in lineas:
        for m in re.finditer(r"(?:^|[\s($])aws\s+([a-z0-9-]+)\s+([a-z0-9-]+)(.*)", linea):
            servicio, operacion, resto = m.groups()
            # El comando termina en una tubería, un paréntesis de cierre, ; o &&
            resto = re.split(r"\s\|\s|\)|;|&&", resto)[0]
            opciones = re.findall(r"(?:^|\s)--([a-z0-9-]+)", resto)
            yield servicio, operacion, opciones


def casos():
    for script in SCRIPTS:
        texto = script.read_text(encoding="utf-8")
        for servicio, operacion, opciones in comandos(texto):
            ruta = script.relative_to(RAIZ).as_posix()
            yield pytest.param(servicio, operacion, opciones, id=f"{ruta}: aws {servicio} {operacion}")


@pytest.mark.parametrize("servicio,operacion,opciones", list(casos()))
def test_comando_aws_valido(servicio, operacion, opciones):
    if servicio == "configure":  # comando propio de la CLI (aws configure get/set/sso...)
        return
    if servicio == "s3":
        assert operacion in S3_ALTO_NIVEL, f"`aws s3 {operacion}` no existe"
        return

    nombre = SERVICIOS.get(servicio, servicio)
    assert nombre in sesion.get_available_services(), f"servicio desconocido: {servicio}"
    modelo = sesion.get_service_model(nombre)

    if operacion == "wait":
        # aws <servicio> wait <waiter>: el waiter va tras "wait"; aquí no se validan opciones
        return

    por_cli = {xform_name(op, "-"): op for op in modelo.operation_names}
    assert operacion in por_cli, f"`aws {servicio} {operacion}` no existe"

    entrada = modelo.operation_model(por_cli[operacion]).input_shape
    validas = set(OPCIONES_GLOBALES) | PERSONALIZACIONES.get((servicio, operacion), set())
    if entrada is not None:
        validas |= {xform_name(m, "-") for m in entrada.members}
    for opcion in opciones:
        base = opcion[3:] if opcion.startswith("no-") else opcion  # --no-publicly-accessible
        assert opcion in validas or base in validas, f"`aws {servicio} {operacion} --{opcion}` no existe"


def test_waiters_existen():
    for script in SCRIPTS:
        texto = re.sub(r"\\\r?\n", " ", script.read_text(encoding="utf-8"))
        for servicio, waiter in re.findall(r"aws\s+([a-z0-9-]+)\s+wait\s+([a-z0-9-]+)", texto):
            nombre = SERVICIOS.get(servicio, servicio)
            waiters = {xform_name(w, "-") for w in sesion.get_waiter_model(nombre).waiter_names}
            assert waiter in waiters, f"{script.name}: `aws {servicio} wait {waiter}` no existe"
