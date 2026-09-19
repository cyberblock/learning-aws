# 08 · Serverless: AWS Lambda

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11936s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 17:01

**Tramo del vídeo:** 3:18:56 – 3:35:57

| Capítulo | Inicio |
|----------|--------|
| Serverless | [3:18:56](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11936s) |
| Qué es Serverless | [3:19:37](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11977s) |
| AWS Lambda | [3:20:42](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12042s) |
| Lambda demo | [3:26:58](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12418s) |

**Código:** [`08_serverless/`](../08_serverless/): la función de la demo y su despliegue con la CLI.

## Resumen

**Serverless** no significa que no haya servidores: significa que **tú no los gestionas**. Subes código y
AWS se ocupa de dónde y cuándo se ejecuta. **AWS Lambda** es el servicio insignia: funciones que se disparan
por **eventos**, se ejecutan unos segundos y se pagan **por solicitud y por tiempo de cálculo**. Si en el
examen aparece "serverless", piensa en Lambda.

## Qué es serverless

El paradigma empezó como *función como servicio* (FaaS), pero hoy abarca todo lo gestionado: bases de datos,
mensajería, almacenamiento. Lo común es que no hay que aprovisionar ni mantener máquinas.

| | EC2 | Lambda |
|---|-----|--------|
| Qué despliegas | Servidores virtuales | Funciones |
| Límite | CPU y RAM | **Tiempo** de ejecución |
| Funcionamiento | Continuo | **Bajo demanda**, por evento |
| Escalado | Tú añades o quitas instancias | **Automático** |
| Pago | Por tiempo encendido | Por solicitud y por cálculo |

## AWS Lambda

- **Dirigida por eventos:** S3, DynamoDB, API Gateway, EventBridge... cualquiera de ellos puede invocarla.
- **Lenguajes:** Node.js, Python, Java, C#, Go, PowerShell, Ruby y tiempos de ejecución personalizados
  (Rust, por ejemplo). También acepta imágenes de contenedor, siempre que implementen la API de tiempo de
  ejecución de Lambda; para imágenes Docker cualquiera, lo suyo es **ECS o Fargate**.
- **Recursos por función:** hasta **10 GB de RAM**; subir la memoria sube también CPU y red.
- **Monitorización** integrada con **CloudWatch**.

### Precio

| Concepto | Capa gratuita mensual | Después |
|----------|----------------------|---------|
| Solicitudes | 1 000 000 | 0,20 USD por millón |
| Tiempo de cálculo | 400 000 **GB-segundo** | ~0,0000167 USD por GB-segundo |

El **GB-segundo** es memoria × tiempo: una función de 128 MB que corre 1 segundo gasta 0,125 GB-segundo. Con
400 000 GB-segundo gratis tienes unas 3 200 000 segundos de una función de 128 MB. La duración se factura en
incrementos de **1 milisegundo**.

### Ejemplos de uso

- **Miniaturas:** subir una imagen a S3 dispara la función, que genera la miniatura, la guarda en S3 y
  escribe los metadatos (nombre, tamaño, fecha) en DynamoDB.
- **Tarea programada sin servidor:** una regla de **EventBridge** invoca la función cada hora. Es un `cron`
  sin máquina que mantener.

## Demo: crear la función

1. **Crear desde cero**, nombre y **tiempo de ejecución** (Python, versión más reciente).
2. AWS crea solo un **rol de ejecución**, con permiso para escribir registros en CloudWatch.
3. El editor trae un código de ejemplo. Al cambiarlo hay que pulsar **Deploy**: si no, se sigue ejecutando
   el anterior.
4. Pestaña **Probar**: se crea un evento de prueba con nombre, se invoca y se ve el resultado, los registros
   y el resumen de la ejecución. Los eventos de prueba se guardan y se reutilizan.

```python
def lambda_handler(event, context):
    nombre = event.get("nombre", "mundo")
    return {"statusCode": 200, "body": json.dumps({"mensaje": f"Hola {nombre}"})}
```

Lo mismo con la CLI está en [`cli-lambda.sh`](../08_serverless/cli-lambda.sh):

```bash
zip funcion.zip funcion_lambda.py
aws lambda create-function --function-name demo-lambda \
  --runtime python3.13 --role "$ROL_ARN" \
  --handler funcion_lambda.lambda_handler --zip-file fileb://funcion.zip
aws lambda invoke --function-name demo-lambda \
  --payload '{"nombre":"Joan"}' --cli-binary-format raw-in-base64-out respuesta.json
```

### Lo que hay en la consola

| Pestaña | Qué encuentras |
|---------|----------------|
| **Supervisión** | Invocaciones, duración, errores, tasa de éxito y limitaciones |
| **Registros** | Grupo `/aws/lambda/<función>` en CloudWatch Logs: el primer sitio donde mirar un fallo |
| **Configuración → general** | Memoria, almacenamiento y **tiempo de espera** (3 segundos por defecto) |
| **Configuración → desencadenadores** | Qué servicio invoca la función (S3, EventBridge, API Gateway...) |
| **Configuración → permisos** | El **rol de ejecución** y lo que la función puede hacer |

### El rol de ejecución

El rol que se crea solo permite **escribir registros**. Para que la función lea un bucket de S3 o escriba en
DynamoDB hay que **añadir permisos a ese rol**. Es la causa número uno de errores del tipo *AccessDenied* en
las primeras funciones.

> **Nota de precisión.** Un rol tiene dos políticas distintas: la **de confianza** (quién puede asumirlo; en
> Lambda, el servicio `lambda.amazonaws.com`) y las **de permisos** (qué puede hacer). Están separadas, y es
> la de permisos la que hay que ampliar. Ejemplo de la de confianza:
> [`politica-rol-lambda.json`](../08_serverless/politica-rol-lambda.json).

> **Nota de precisión.** El **tiempo de espera** máximo de una función es de **15 minutos** (900 segundos),
> con 3 segundos por defecto. Para trabajos más largos: ECS, Fargate, Batch o Step Functions.

> **Nota de precisión.** "Sin servidor" tampoco quiere decir "sin latencia": la primera invocación tras un
> rato parada sufre un **arranque en frío**. Se nota sobre todo en Java y .NET.

## Errores típicos

- Cambiar el código y no pulsar **Deploy**.
- Dejar el tiempo de espera en 3 segundos para una tarea que necesita más.
- Esperar que la función acceda a S3 o DynamoDB sin ampliar el rol de ejecución.
- No mirar CloudWatch Logs cuando algo falla.
- Confundir "serverless" con "no hay servidores".

## Ejercicios

En [`08_serverless/ejercicios`](../08_serverless/ejercicios/):

1. Calcula los GB-segundo de una invocación.
2. Valida la configuración de una función (memoria y tiempo de espera).
3. Calcula el coste mensual del tiempo de cálculo con la capa gratuita.
4. **Arregla este código:** el coste de las solicitudes, que ignora el millón gratuito y aplica el precio
   del millón a cada solicitud.
