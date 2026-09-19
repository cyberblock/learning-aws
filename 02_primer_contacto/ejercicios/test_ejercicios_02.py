# Tests de los ejercicios 02. Por defecto prueban soluciones_02.py; con --mios, ejercicios_02.py.
import botocore.session
from botocore.validate import ParamValidator

ENTRADA = botocore.session.get_session().get_service_model("budgets").operation_model("CreateBudget").input_shape


def valida_contra_api(datos, miembro):
    informe = ParamValidator().validate(datos, ENTRADA.members[miembro])
    assert not informe.has_errors(), informe.generate_report()


def test_umbral_en_dolares(ej):
    assert ej.umbral_en_dolares(10, 50) == 5.0
    assert ej.umbral_en_dolares(25, 80) == 20.0
    assert ej.umbral_en_dolares(10, 33) == 3.3


def test_construir_presupuesto(ej):
    presupuesto = ej.construir_presupuesto("presupuesto-mensual", 10)
    valida_contra_api(presupuesto, "Budget")
    assert presupuesto["BudgetLimit"] == {"Amount": "10", "Unit": "USD"}
    assert presupuesto["TimeUnit"] == "MONTHLY"
    assert presupuesto["BudgetType"] == "COST"


def test_construir_notificacion(ej):
    notificacion = ej.construir_notificacion("yo@example.com", 50)
    valida_contra_api([notificacion], "NotificationsWithSubscribers")
    assert notificacion["Notification"]["Threshold"] == 50
    assert notificacion["Notification"]["ThresholdType"] == "PERCENTAGE"
    assert notificacion["Subscribers"][0]["Address"] == "yo@example.com"


def test_alertas_disparadas(ej):
    assert ej.alertas_disparadas(5, 10, [80, 50, 100]) == [50]
    assert ej.alertas_disparadas(10, 10, [100, 50, 80]) == [50, 80, 100]
    assert ej.alertas_disparadas(0, 10, [50]) == []
    assert ej.alertas_disparadas(4.99, 10, [50]) == []
