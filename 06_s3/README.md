# 06 · Almacenamiento de objetos (S3)

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8852s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 2:27:32 – 2:41:29
- **Apunte:** [apuntes/06-s3.md](../apuntes/06-s3.md)

En el vídeo todo se hace desde la consola. El script es el equivalente con la AWS CLI y **no aparece en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `cli-s3.sh` | Crear el bucket, bloquear el acceso público, activar versionado, subir objetos y firmar una URL |
| `politica-bucket-lectura-publica.json` | Política de bucket que deja leer los objetos al público (para un sitio estático) |
| `ejercicios/` | Nombres de bucket, claves y prefijos, subida multiparte y listar una "carpeta" (arregla el código) |

> Los `.json` no admiten comentarios, así que la referencia al vídeo y al apunte de esos archivos está en este README.
> ⚠️ El nombre del bucket es **único en todo AWS**: cambia `BUCKET` en el script antes de ejecutarlo. La
> política pública solo tiene efecto si antes quitas el bloqueo de acceso público: úsala a conciencia.
