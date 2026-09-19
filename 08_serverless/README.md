# 08 · Serverless: AWS Lambda

- **Vídeo:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11936s), de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)
- **Tramo:** 3:18:56 – 3:35:57
- **Apunte:** [apuntes/08-serverless-lambda.md](../apuntes/08-serverless-lambda.md)

En el vídeo la función se escribe en el editor de la consola. Aquí está el mismo código como archivo, más el
despliegue equivalente con la AWS CLI, que **no aparece en el vídeo**.

| Archivo | Qué es |
|---------|--------|
| `funcion_lambda.py` | El manejador (`lambda_handler`): recibe el evento y devuelve la respuesta |
| `politica-rol-lambda.json` | Política de confianza del rol de ejecución: permite que Lambda lo asuma |
| `cli-lambda.sh` | Crea el rol, empaqueta el código, despliega la función, la invoca y busca sus registros |
| `ejercicios/` | GB-segundo, límites de configuración y las dos partes del precio (arregla el código) |

> Los `.json` no admiten comentarios, así que la referencia al vídeo y al apunte de esos archivos está en este README.
> El `.zip` y `respuesta-lambda.json` que genera el script están en `.gitignore`.
