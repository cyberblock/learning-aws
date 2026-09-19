# Tests de los ejercicios 08. Por defecto prueban soluciones_08.py; con --mios, ejercicios_08.py.


def test_gb_segundos(ej):
    assert ej.gb_segundos(1000, 1024) == 1.0
    assert ej.gb_segundos(500, 1024) == 0.5
    assert ej.gb_segundos(1000, 128) == 0.125


def test_configuracion_valida(ej):
    assert ej.configuracion_valida(128, 3) is True
    assert ej.configuracion_valida(10240, 900) is True
    assert ej.configuracion_valida(64, 3) is False       # poca memoria
    assert ej.configuracion_valida(20480, 3) is False    # demasiada memoria
    assert ej.configuracion_valida(128, 901) is False    # más de 15 minutos
    assert ej.configuracion_valida(128, 0) is False


def test_coste_computo(ej):
    assert ej.coste_computo(400_000) == 0.0
    assert ej.coste_computo(0) == 0.0
    assert ej.coste_computo(500_000) == round(100_000 * 0.0000166667, 6)


def test_coste_solicitudes(ej):
    assert ej.coste_solicitudes(1_000_000) == 0.0
    assert ej.coste_solicitudes(500_000) == 0.0
    assert ej.coste_solicitudes(3_000_000) == 0.4
    assert ej.coste_solicitudes(1_500_000) == 0.1
