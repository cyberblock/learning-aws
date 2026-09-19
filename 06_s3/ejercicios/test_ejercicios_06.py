# Tests de los ejercicios 06. Por defecto prueban soluciones_06.py; con --mios, ejercicios_06.py.
import pytest

GIB = 1024 ** 3
TIB = 1024 ** 4


def test_nombre_valido(ej):
    assert ej.nombre_valido("demo-curso-aws-2026") is True
    assert ej.nombre_valido("ab") is False                 # menos de 3 caracteres
    assert ej.nombre_valido("a" * 64) is False             # más de 63
    assert ej.nombre_valido("Demo-Curso") is False         # mayúsculas
    assert ej.nombre_valido("demo_curso") is False         # guion bajo
    assert ej.nombre_valido("-demo-curso") is False        # no empieza por letra o número
    assert ej.nombre_valido("demo-curso-") is False        # no termina por letra o número
    assert ej.nombre_valido("192.168.1.1") is False        # parece una IP
    assert ej.nombre_valido("xn--demo-curso") is False
    assert ej.nombre_valido("demo-curso-s3alias") is False


def test_partir_clave(ej):
    assert ej.partir_clave("mi-carpeta/otra/mi-archivo.txt") == ("mi-carpeta/otra/", "mi-archivo.txt")
    assert ej.partir_clave("mi-archivo.txt") == ("", "mi-archivo.txt")
    assert ej.partir_clave("images/cafe.jpg") == ("images/", "cafe.jpg")


def test_forma_de_subida(ej):
    assert ej.forma_de_subida(1024) == "simple"
    assert ej.forma_de_subida(5 * GIB) == "simple"
    assert ej.forma_de_subida(5 * GIB + 1) == "multiparte"
    assert ej.forma_de_subida(5 * TIB) == "multiparte"
    with pytest.raises(ValueError):
        ej.forma_de_subida(5 * TIB + 1)


def test_objetos_directos(ej):
    claves = ["a.txt", "images/b.jpg", "images/sub/c.jpg", "images-viejas/d.jpg"]
    assert ej.objetos_directos(claves, "images/") == ["images/b.jpg"]
    assert ej.objetos_directos(claves, "") == ["a.txt"]
    assert ej.objetos_directos(claves, "sin-nada/") == []
