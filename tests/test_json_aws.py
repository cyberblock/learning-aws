"""Valida los archivos .json del repositorio sin conectarse a AWS.

- Los que se pasan a la CLI se validan contra el modelo de botocore de la operación.
- Las políticas IAM se validan con una comprobación estructural básica.
- Cada .json debe aparecer en ESQUEMAS: así ninguno se queda sin validar.
"""

import json
from pathlib import Path

import botocore.session
import pytest
from botocore.validate import ParamValidator

RAIZ = Path(__file__).resolve().parent.parent

# ruta -> (servicio, operación, miembro de la entrada) | "politica-iam" | "libre"
ESQUEMAS = {
    "02_primer_contacto/presupuesto.json": ("budgets", "CreateBudget", "Budget"),
    "02_primer_contacto/notificaciones.json": (
        "budgets",
        "CreateBudget",
        "NotificationsWithSubscribers",
    ),
    "03_iam/politica-solo-lectura.json": "politica-iam",
}

sesion = botocore.session.get_session()


def validar_politica_iam(doc):
    assert doc.get("Version") == "2012-10-17", "Version debe ser 2012-10-17"
    sentencias = doc["Statement"]
    sentencias = sentencias if isinstance(sentencias, list) else [sentencias]
    for s in sentencias:
        assert s["Effect"] in ("Allow", "Deny")
        assert "Action" in s or "NotAction" in s
        # Las políticas de confianza usan Principal en lugar de Resource
        assert "Resource" in s or "NotResource" in s or "Principal" in s


def archivos_json():
    return sorted(RAIZ.glob("[0-9][0-9]_*/**/*.json"))


@pytest.mark.parametrize("ruta", archivos_json(), ids=lambda p: p.relative_to(RAIZ).as_posix())
def test_json_valido(ruta):
    clave = ruta.relative_to(RAIZ).as_posix()
    assert clave in ESQUEMAS, f"añade {clave} a ESQUEMAS en tests/test_json_aws.py"
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    esquema = ESQUEMAS[clave]

    if esquema == "libre":
        return
    if esquema == "politica-iam":
        validar_politica_iam(datos)
        return

    servicio, operacion, miembro = esquema
    forma = sesion.get_service_model(servicio).operation_model(operacion).input_shape
    forma = forma.members[miembro]
    informe = ParamValidator().validate(datos, forma)
    assert not informe.has_errors(), informe.generate_report()
