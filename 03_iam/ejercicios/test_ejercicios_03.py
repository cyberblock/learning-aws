# Tests de los ejercicios 03. Por defecto prueban soluciones_03.py; con --mios, ejercicios_03.py.
import json
from pathlib import Path

import pytest

POLITICA = json.loads(
    (Path(__file__).resolve().parent.parent / "politica-solo-lectura.json").read_text(encoding="utf-8")
)

ADMIN = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}],
}


def test_construir_politica(ej):
    politica = ej.construir_politica(["ec2:DescribeInstances"])
    assert politica["Version"] == "2012-10-17"
    sentencia = politica["Statement"][0]
    assert sentencia["Effect"] == "Allow"
    assert sentencia["Action"] == ["ec2:DescribeInstances"]
    assert sentencia["Resource"] == "*"


def test_url_inicio_sesion(ej):
    assert ej.url_inicio_sesion("joan-aws") == "https://joan-aws.signin.aws.amazon.com/console"
    assert ej.url_inicio_sesion("", "123456789012") == "https://123456789012.signin.aws.amazon.com/console"
    with pytest.raises(ValueError):
        ej.url_inicio_sesion(None)


def test_permite(ej):
    assert ej.permite(POLITICA, "ec2:DescribeInstances") is True
    assert ej.permite(POLITICA, "cloudwatch:GetMetricStatistics") is True
    assert ej.permite(POLITICA, "ec2:RunInstances") is False
    assert ej.permite(POLITICA, "s3:ListBucket") is False
    assert ej.permite(ADMIN, "s3:DeleteBucket") is True


def test_es_administrador(ej):
    assert ej.es_administrador(ADMIN) is True
    assert ej.es_administrador(POLITICA) is False
    # Solo recursos "*" no basta: las acciones siguen estando limitadas
    solo_recursos = {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}]}
    assert ej.es_administrador(solo_recursos) is False
    # Un Deny total no concede nada
    deny = {"Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}]}
    assert ej.es_administrador(deny) is False
    # Action y Resource como listas
    listas = {"Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": ["*"]}]}
    assert ej.es_administrador(listas) is True
