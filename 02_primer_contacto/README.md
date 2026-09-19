# 02 · Primer contacto con AWS

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 0:34:12 – 0:53:05
- **Apunte:** [apuntes/02-primer-contacto-aws.md](../apuntes/02-primer-contacto-aws.md)

En el vídeo todo se hace desde la consola. Los scripts son el equivalente con la AWS CLI y **no aparecen en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `presupuesto.json` | Presupuesto de costes de 10 USD/mes (el de la demo) |
| `notificaciones.json` | Alerta por correo al 50 % del gasto real. Cambia la dirección antes de usarlo |
| `cli-presupuesto.sh` | Crea el presupuesto con `aws budgets create-budget` |
| `cli-regiones.sh` | Lista regiones y zonas de disponibilidad (solo consulta) |
| `ejercicios/` | Umbrales, JSON del presupuesto y de la notificación, alertas disparadas (arregla el código) |

> Los `.json` no admiten comentarios, así que la referencia al vídeo y al apunte de esos archivos está en este README.
