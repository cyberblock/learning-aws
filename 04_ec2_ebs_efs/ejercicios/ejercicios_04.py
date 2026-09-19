# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo 1:07:09–1:47:33: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Ejercicios 04 · EC2, EBS y EFS
# Sustituye cada `raise NotImplementedError` por tu código y comprueba con:
#     pytest 04_ec2_ebs_efs --mios


# 1. Coste mensual de un volumen EBS. Se factura la capacidad APROVISIONADA, se use o no.
#    coste_ebs_mensual(100, 12, 0.08) -> 8.0   (100 GiB aprovisionados, 12 usados)
#    Redondea a 2 decimales.
def coste_ebs_mensual(gb_aprovisionados, gb_usados, precio_por_gb):
    raise NotImplementedError("ejercicio 1")


# 2. ¿Se puede adjuntar este volumen a esta instancia? Reglas de EBS:
#    - el volumen y la instancia deben estar en la MISMA zona de disponibilidad;
#    - un volumen solo puede estar adjunto a una instancia a la vez.
#    Los dicts son así:
#       volumen   = {"az": "us-east-1a", "instancia": None}   # o el id de la instancia
#       instancia = {"az": "us-east-1a"}
def puede_adjuntarse(volumen, instancia):
    raise NotImplementedError("ejercicio 2")


# 3. Construye la lista de políticas de ciclo de vida de EFS para `aws efs put-lifecycle-configuration`:
#    pasar a EFS-IA tras `dias` sin acceso y volver a la clase estándar al primer acceso.
#    politica_efs(60) -> [{"TransitionToIA": "AFTER_60_DAYS"},
#                         {"TransitionToPrimaryStorageClass": "AFTER_1_ACCESS"}]
#    Solo valen estos valores de días: 1, 7, 14, 30, 60, 90, 180, 270, 365.
#    Con 1 día el texto es "AFTER_1_DAY" (singular); con cualquier otro número no válido,
#    lanza ValueError.
def politica_efs(dias):
    raise NotImplementedError("ejercicio 3")


# 4. ARREGLA ESTE CÓDIGO. Devuelve los nombres de dispositivo de los volúmenes que SOBREVIVEN
#    al terminar la instancia, en el orden en que llegan.
#    Regla: sobrevive el que tiene "borrar_al_terminar" en False. Si el campo no está,
#    vale el valor por defecto: el volumen RAÍZ se borra y los demás se conservan.
#    volumenes = [{"dispositivo": "/dev/xvda", "raiz": True},
#                 {"dispositivo": "/dev/sdf", "raiz": False}]   -> ["/dev/sdf"]
def volumenes_que_sobreviven(volumenes):
    sobreviven = []
    for volumen in volumenes:
        if volumen["borrar_al_terminar"]:
            sobreviven.append(volumen["dispositivo"])
    return sobreviven
