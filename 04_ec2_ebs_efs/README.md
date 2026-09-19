# 04 · Computación: EC2, EBS y EFS

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 1:07:09 – 1:47:33
- **Apunte:** [apuntes/04-ec2-ebs-efs.md](../apuntes/04-ec2-ebs-efs.md)

En el vídeo las demos se hacen desde la consola; el único código que aparece es el script de datos de
usuario. Los scripts `cli-*.sh` son el equivalente con la AWS CLI y **no aparecen en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `user-data.sh` | Script de arranque: instala Apache y publica "Hola mundo" con el nombre de la instancia |
| `cli-instancia-ec2.sh` | Par de claves, grupo de seguridad y lanzamiento de la instancia con `user-data.sh` |
| `cli-volumen-ebs.sh` | Crea un volumen EBS en la zona de la instancia, lo adjunta y toca *delete on termination* |
| `cli-efs.sh` | Sistema de archivos EFS, punto de montaje y regla de ciclo de vida a EFS-IA |
| `ejercicios/` | Coste aprovisionado, reglas de adjuntar un volumen, ciclo de vida de EFS y supervivencia de volúmenes (arregla el código) |

> ⚠️ Estos scripts **crean recursos que cuestan dinero**. Cada uno lleva su bloque de limpieza comentado al
> final: ejecútalo cuando termines y comprueba en la consola que no queda nada encendido.
