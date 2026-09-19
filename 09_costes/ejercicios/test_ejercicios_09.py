# Tests de los ejercicios 09. Por defecto prueban soluciones_09.py; con --mios, ejercicios_09.py.
import csv
from pathlib import Path

import pytest

CSV_EJEMPLO = Path(__file__).resolve().parent.parent / "costes-ejemplo.csv"


@pytest.fixture
def filas():
    with CSV_EJEMPLO.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def test_coste_por_servicio(ej, filas):
    costes = ej.coste_por_servicio(filas)
    assert costes["Amazon EC2"] == 10.6
    assert costes["Amazon S3"] == 0.35
    assert costes["Elastic Load Balancing"] == 1.2
    assert costes["AWS Lambda"] == 0.0
    assert round(sum(costes.values()), 2) == 15.4


def test_top_servicios(ej):
    costes = {"Amazon EC2": 10.6, "Amazon RDS": 2.75, "Amazon S3": 0.35, "AWS Lambda": 0.35}
    assert ej.top_servicios(costes, 2) == [("Amazon EC2", 10.6), ("Amazon RDS", 2.75)]
    # A igualdad de coste, orden alfabético
    assert ej.top_servicios(costes, 4)[2:] == [("AWS Lambda", 0.35), ("Amazon S3", 0.35)]


def test_prevision_fin_de_mes(ej):
    assert ej.prevision_fin_de_mes(15.4, 4, 30) == 115.5
    assert ej.prevision_fin_de_mes(10, 10, 30) == 30.0
    with pytest.raises(ValueError):
        ej.prevision_fin_de_mes(0, 0, 30)


def test_etiquetas_de_usuario(ej, filas):
    etiquetas = [fila["etiqueta"] for fila in filas]
    assert ej.etiquetas_de_usuario(etiquetas) == ["department"]
    mezcla = ["user:proyecto$web", "user:department$IT", "aws:cloudformation:stack-name$demo"]
    assert ej.etiquetas_de_usuario(mezcla) == ["department", "proyecto"]
    assert ej.etiquetas_de_usuario(["aws:createdBy$IAMUser"]) == []
