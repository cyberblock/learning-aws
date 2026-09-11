# Tests de los ejercicios 01. Por defecto prueban soluciones_01.py; con --mios, ejercicios_01.py.
import pytest


def test_clasificar_servicio(ej):
    assert ej.clasificar_servicio("EC2") == "IaaS"
    assert ej.clasificar_servicio("  elastic beanstalk ") == "PaaS"
    assert ej.clasificar_servicio("Gmail") == "SaaS"
    assert ej.clasificar_servicio("Rekognition") == "SaaS"
    assert ej.clasificar_servicio("lambda") == "FaaS"
    with pytest.raises(ValueError):
        ej.clasificar_servicio("Excel en mi portátil")


def test_quien_gestiona(ej):
    assert ej.quien_gestiona("red", "on-premises") == "tú"
    assert ej.quien_gestiona("sistema operativo", "IaaS") == "tú"
    assert ej.quien_gestiona("virtualizacion", "IaaS") == "proveedor"
    assert ej.quien_gestiona("datos", "PaaS") == "tú"
    assert ej.quien_gestiona("runtime", "PaaS") == "proveedor"
    assert ej.quien_gestiona("aplicaciones", "SaaS") == "proveedor"


def test_coste_semanal(ej):
    assert ej.coste_semanal(100, 20, 0.10) == {"fijo": 1680.0, "elastico": 1296.0, "ahorro": 384.0}
    # Sin variación de carga, la elasticidad no ahorra nada
    assert ej.coste_semanal(10, 10, 1.0)["ahorro"] == 0


REGIONES = [
    {"codigo": "us-east-1", "zona": "EEUU", "latencia_ms": 95, "precio": 1.00, "servicios": {"ec2", "s3", "lambda"}},
    {"codigo": "eu-west-1", "zona": "UE", "latencia_ms": 30, "precio": 1.10, "servicios": {"ec2", "s3", "lambda"}},
    {"codigo": "eu-south-2", "zona": "UE", "latencia_ms": 12, "precio": 1.15, "servicios": {"ec2", "s3"}},
    {"codigo": "eu-west-3", "zona": "UE", "latencia_ms": 30, "precio": 1.05, "servicios": {"ec2", "s3", "lambda"}},
]


def test_elegir_region_respeta_la_zona_y_los_servicios(ej):
    # La más barata es us-east-1, pero los datos deben quedarse en la UE
    # y eu-south-2 (la más cercana) no tiene Lambda. Empate a 30 ms: gana la más barata.
    assert ej.elegir_region(REGIONES, "UE", {"ec2", "lambda"}) == "eu-west-3"


def test_elegir_region_sin_restriccion_legal_prioriza_latencia(ej):
    assert ej.elegir_region(REGIONES, None, {"ec2"}) == "eu-south-2"


def test_elegir_region_sin_candidatas(ej):
    assert ej.elegir_region(REGIONES, "UE", {"rekognition"}) is None
    assert ej.elegir_region([], None, set()) is None
