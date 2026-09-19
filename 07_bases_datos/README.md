# 07 · Bases de datos: RDS, Aurora y DynamoDB

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9689s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 2:41:29 – 3:18:56
- **Apunte:** [apuntes/07-bases-de-datos.md](../apuntes/07-bases-de-datos.md)

En el vídeo todo se hace desde la consola. Los scripts son el equivalente con la AWS CLI y **no aparecen en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `cli-rds.sh` | Instancia MySQL de la capa gratuita sin acceso público, con copias y una instantánea |
| `cli-dynamodb.sh` | Tabla con clave de partición, dos elementos con atributos distintos y consultas |
| `item-usuario.json` | Un elemento de DynamoDB en formato de atributos (`S`, `N`, `BOOL`) |
| `ejercicios/` | Relacional o no, conversión a atributos de DynamoDB, nombres de tabla y esquema libre (arregla el código) |

> Los `.json` no admiten comentarios, así que la referencia al vídeo y al apunte de esos archivos está en este README.
> ⚠️ `cli-rds.sh` pide la contraseña por teclado: no la escribas en el archivo. Una base de datos olvidada
> encendida es la factura sorpresa más habitual.
