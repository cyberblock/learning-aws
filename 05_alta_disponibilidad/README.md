# 05 · Alta disponibilidad: ELB y Auto Scaling

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 1:47:33 – 2:27:32
- **Apunte:** [apuntes/05-alta-disponibilidad.md](../apuntes/05-alta-disponibilidad.md)

En el vídeo todo se hace desde la consola. Los scripts son el equivalente con la AWS CLI y **no aparecen en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `cli-alb.sh` | Application Load Balancer: grupo de seguridad, grupo de destino, agente de escucha y registro de instancias |
| `cli-asg.sh` | Plantilla de lanzamiento y grupo de autoescalado (1/2/4) conectado al grupo de destino |
| `ejercicios/` | Escalado vertical u horizontal, límites de capacidad, reparto por turnos y alta disponibilidad (arregla el código) |

El script de arranque de las instancias es el del módulo anterior: [`04_ec2_ebs_efs/user-data.sh`](../04_ec2_ebs_efs/user-data.sh).

> ⚠️ Un balanceador cuesta por hora aunque no reciba tráfico. Para limpiar, **primero el grupo de
> autoescalado** (si no, vuelve a lanzar las instancias que termines), luego el balanceador, el grupo de
> destino y por último las instancias.
