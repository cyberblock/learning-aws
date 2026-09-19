# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 1:07:09–1:47:33: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Soluciones de los ejercicios 04 · EC2, EBS y EFS

DIAS_VALIDOS = (1, 7, 14, 30, 60, 90, 180, 270, 365)


def coste_ebs_mensual(gb_aprovisionados, gb_usados, precio_por_gb):
    return round(gb_aprovisionados * precio_por_gb, 2)


def puede_adjuntarse(volumen, instancia):
    if volumen.get("instancia"):
        return False
    return volumen["az"] == instancia["az"]


def politica_efs(dias):
    if dias not in DIAS_VALIDOS:
        raise ValueError(f"EFS solo admite {DIAS_VALIDOS} días, no {dias}")
    unidad = "DAY" if dias == 1 else "DAYS"
    return [
        {"TransitionToIA": f"AFTER_{dias}_{unidad}"},
        {"TransitionToPrimaryStorageClass": "AFTER_1_ACCESS"},
    ]


def volumenes_que_sobreviven(volumenes):
    sobreviven = []
    for volumen in volumenes:
        por_defecto = not volumen.get("raiz", False)
        conservar = not volumen.get("borrar_al_terminar", not por_defecto)
        if conservar:
            sobreviven.append(volumen["dispositivo"])
    return sobreviven
