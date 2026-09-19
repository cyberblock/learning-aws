# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "Lambda demo" 3:26:58: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12418s
# Apunte: apuntes/08-serverless-lambda.md
#
# Función Lambda de la demo: devuelve un saludo. El manejador recibe el evento que
# dispara la ejecución y un contexto con datos de la propia invocación.

import json


def lambda_handler(event, context):
    nombre = event.get("nombre", "mundo")
    print(f"Invocación {context.aws_request_id if context else 'local'} para {nombre}")
    return {
        "statusCode": 200,
        "body": json.dumps({"mensaje": f"Hola {nombre}"}, ensure_ascii=False),
    }
