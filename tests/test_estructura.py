"""Comprueba que cada plantilla de ejercicios tiene las mismas funciones que sus soluciones."""

import ast
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLAS = sorted(RAIZ.glob("[0-9][0-9]_*/ejercicios/ejercicios_*.py"))


def funciones(ruta):
    arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    return {
        n.name: [a.arg for a in n.args.args]
        for n in arbol.body
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")
    }


@pytest.mark.parametrize("plantilla", PLANTILLAS, ids=lambda p: p.name)
def test_plantilla_coincide_con_soluciones(plantilla):
    soluciones = plantilla.with_name(plantilla.name.replace("ejercicios_", "soluciones_"))
    tests = plantilla.with_name("test_" + plantilla.name)
    assert soluciones.exists(), f"falta {soluciones.name}"
    assert tests.exists(), f"falta {tests.name}"
    assert funciones(plantilla) == funciones(soluciones)


def test_cada_modulo_tiene_readme():
    for carpeta in RAIZ.glob("[0-9][0-9]_*"):
        assert (carpeta / "README.md").exists(), f"falta {carpeta.name}/README.md"
