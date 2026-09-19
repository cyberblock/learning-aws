# Tests de los ejercicios 04. Por defecto prueban soluciones_04.py; con --mios, ejercicios_04.py.
import botocore.session
import pytest
from botocore.validate import ParamValidator

ENTRADA = (
    botocore.session.get_session()
    .get_service_model("efs")
    .operation_model("PutLifecycleConfiguration")
    .input_shape
)


def test_coste_ebs_mensual(ej):
    assert ej.coste_ebs_mensual(100, 12, 0.08) == 8.0
    assert ej.coste_ebs_mensual(2, 0, 0.08) == 0.16
    # Se paga lo aprovisionado: usar menos no abarata
    assert ej.coste_ebs_mensual(100, 100, 0.08) == ej.coste_ebs_mensual(100, 1, 0.08)


def test_puede_adjuntarse(ej):
    libre = {"az": "us-east-1a", "instancia": None}
    assert ej.puede_adjuntarse(libre, {"az": "us-east-1a"}) is True
    assert ej.puede_adjuntarse(libre, {"az": "us-east-1b"}) is False
    ocupado = {"az": "us-east-1a", "instancia": "i-0123456789abcdef0"}
    assert ej.puede_adjuntarse(ocupado, {"az": "us-east-1a"}) is False


def test_politica_efs(ej):
    politicas = ej.politica_efs(60)
    entrada = {"FileSystemId": "fs-0123456789abcdef0", "LifecyclePolicies": politicas}
    informe = ParamValidator().validate(entrada, ENTRADA)
    assert not informe.has_errors(), informe.generate_report()
    assert politicas[0] == {"TransitionToIA": "AFTER_60_DAYS"}
    assert politicas[1] == {"TransitionToPrimaryStorageClass": "AFTER_1_ACCESS"}
    assert ej.politica_efs(1)[0] == {"TransitionToIA": "AFTER_1_DAY"}
    with pytest.raises(ValueError):
        ej.politica_efs(45)


def test_volumenes_que_sobreviven(ej):
    volumenes = [
        {"dispositivo": "/dev/xvda", "raiz": True},
        {"dispositivo": "/dev/sdf", "raiz": False},
    ]
    assert ej.volumenes_que_sobreviven(volumenes) == ["/dev/sdf"]
    # Con el valor explícito manda el valor explícito
    explicitos = [
        {"dispositivo": "/dev/xvda", "raiz": True, "borrar_al_terminar": False},
        {"dispositivo": "/dev/sdf", "raiz": False, "borrar_al_terminar": True},
    ]
    assert ej.volumenes_que_sobreviven(explicitos) == ["/dev/xvda"]
    assert ej.volumenes_que_sobreviven([]) == []
