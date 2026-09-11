"""Configuración común de pytest.

Cada carpeta NN_tema/ejercicios/ tiene tres archivos:
- ejercicios_NN.py  -> plantilla para que la rellenes
- soluciones_NN.py  -> soluciones
- test_ejercicios_NN.py -> tests que usan el fixture `ej`

Por defecto los tests se ejecutan contra las soluciones. Con `--mios` se ejecutan contra
tu plantilla: los ejercicios que aún no hayas resuelto fallan con NotImplementedError.
"""

import importlib

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--mios",
        action="store_true",
        help="comprueba tus ejercicios (ejercicios_NN.py) en lugar de las soluciones",
    )


@pytest.fixture
def ej(request):
    numero = request.module.__name__.rsplit("_", 1)[-1]  # test_ejercicios_04 -> "04"
    modulo = "ejercicios" if request.config.getoption("--mios") else "soluciones"
    return importlib.import_module(f"{modulo}_{numero}")
