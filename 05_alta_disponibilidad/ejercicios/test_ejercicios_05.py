# Tests de los ejercicios 05. Por defecto prueban soluciones_05.py; con --mios, ejercicios_05.py.


def test_tipo_de_escalado(ej):
    micro = {"tipo": "t2.micro", "instancias": 1}
    assert ej.tipo_de_escalado(micro, {"tipo": "t2.large", "instancias": 1}) == "vertical"
    assert ej.tipo_de_escalado(micro, {"tipo": "t2.micro", "instancias": 5}) == "horizontal"
    assert ej.tipo_de_escalado(micro, {"tipo": "t2.micro", "instancias": 1}) == "ninguno"
    assert ej.tipo_de_escalado(micro, {"tipo": "t2.large", "instancias": 5}) == "mixto"


def test_capacidad_objetivo(ej):
    assert ej.capacidad_objetivo(2, 1, 4, 5) == 4
    assert ej.capacidad_objetivo(2, 1, 4, -5) == 1
    assert ej.capacidad_objetivo(2, 1, 4, 1) == 3
    assert ej.capacidad_objetivo(2, 1, 4, 0) == 2


def test_reparto(ej):
    dos_sanos = [{"id": "i-a", "estado": "healthy"}, {"id": "i-b", "estado": "healthy"}]
    assert ej.reparto(dos_sanos, 4) == ["i-a", "i-b", "i-a", "i-b"]
    uno_caido = [{"id": "i-a", "estado": "healthy"}, {"id": "i-b", "estado": "unhealthy"}]
    assert ej.reparto(uno_caido, 3) == ["i-a", "i-a", "i-a"]
    assert ej.reparto([{"id": "i-a", "estado": "unhealthy"}], 2) == []


def test_es_alta_disponibilidad(ej):
    una_zona = [
        {"id": "i-a", "az": "us-east-1a", "estado": "healthy"},
        {"id": "i-b", "az": "us-east-1a", "estado": "healthy"},
    ]
    assert ej.es_alta_disponibilidad(una_zona) is False
    dos_zonas = [
        {"id": "i-a", "az": "us-east-1a", "estado": "healthy"},
        {"id": "i-b", "az": "us-east-1b", "estado": "healthy"},
    ]
    assert ej.es_alta_disponibilidad(dos_zonas) is True
    # La segunda zona no cuenta si su instancia está caída
    caida = [
        {"id": "i-a", "az": "us-east-1a", "estado": "healthy"},
        {"id": "i-b", "az": "us-east-1b", "estado": "unhealthy"},
    ]
    assert ej.es_alta_disponibilidad(caida) is False
    assert ej.es_alta_disponibilidad([]) is False
