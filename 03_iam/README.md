# 03 · Seguridad e IAM

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 0:53:05 – 1:07:09
- **Apunte:** [apuntes/03-seguridad-iam.md](../apuntes/03-seguridad-iam.md)

En el vídeo todo se hace desde la consola. Los scripts son el equivalente con la AWS CLI y **no aparecen en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `politica-solo-lectura.json` | Política de solo lectura de EC2, ELB y CloudWatch (la del ejemplo del vídeo) |
| `cli-usuario-iam.sh` | Grupo `admin`, usuario IAM con contraseña de un solo uso y alias de cuenta |
| `cli-politica-propia.sh` | Crea la política del JSON y la adjunta a un grupo de solo lectura |
| `ejercicios/` | Construir políticas, URL de acceso, comodines de acciones y detectar permisos de administrador (arregla el código) |

> Los `.json` no admiten comentarios, así que la referencia al vídeo y al apunte de esos archivos está en este README.
> ⚠️ `cli-usuario-iam.sh` crea identidades reales. El alias de cuenta es único en todo AWS: cámbialo antes de ejecutarlo.
