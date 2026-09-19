# Tests de los ejercicios 07. Por defecto prueban soluciones_07.py; con --mios, ejercicios_07.py.
import botocore.session
import pytest
from botocore.validate import ParamValidator

ENTRADA = (
    botocore.session.get_session()
    .get_service_model("dynamodb")
    .operation_model("PutItem")
    .input_shape
)


def test_tipo_de_base_de_datos(ej):
    assert ej.tipo_de_base_de_datos({"consultas_sql": True}) == "relacional"
    assert ej.tipo_de_base_de_datos({"relaciones": True}) == "relacional"
    assert ej.tipo_de_base_de_datos({"esquema_fijo": True}) == "relacional"
    assert ej.tipo_de_base_de_datos({"formato": "json"}) == "no relacional"
    assert ej.tipo_de_base_de_datos({"consultas_sql": False, "relaciones": False}) == "no relacional"


def test_item_dynamodb(ej):
    item = ej.item_dynamodb(
        {"nombre": "Joan", "edad": 30, "activo": True, "nota": 9.5, "apodo": None}
    )
    assert item["nombre"] == {"S": "Joan"}
    assert item["edad"] == {"N": "30"}
    assert item["activo"] == {"BOOL": True}      # bool antes que número
    assert item["nota"] == {"N": "9.5"}
    assert item["apodo"] == {"NULL": True}
    informe = ParamValidator().validate({"TableName": "demo-usuarios", "Item": item}, ENTRADA)
    assert not informe.has_errors(), informe.generate_report()
    with pytest.raises(TypeError):
        ej.item_dynamodb({"lista": [1, 2, 3]})


def test_nombre_tabla_valido(ej):
    assert ej.nombre_tabla_valido("demo-usuarios") is True
    assert ej.nombre_tabla_valido("Tabla_1.v2") is True
    assert ej.nombre_tabla_valido("ab") is False
    assert ej.nombre_tabla_valido("a" * 256) is False
    assert ej.nombre_tabla_valido("tabla con espacios") is False


def test_atributos(ej):
    items = [{"user_id": 1, "nombre": "Joan"}, {"user_id": 2, "apellido": "Amengual"}]
    assert ej.atributos(items) == ["apellido", "nombre", "user_id"]
    assert ej.atributos([]) == []
    assert ej.atributos([{"b": 1}, {"a": 2}]) == ["a", "b"]
