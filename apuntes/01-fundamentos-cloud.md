# 01 · Fundamentos del cloud

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=0s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 34:12

**Tramo del vídeo:** 0:00:00 – 0:34:12

| Capítulo | Inicio |
|----------|--------|
| Intro al curso | [0:00:00](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=0s) |
| Fundamentos del Cloud | [0:01:52](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=112s) |
| Qué es cloud computing | [0:02:41](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=161s) |
| Tipos cloud computing | [0:13:56](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=836s) |
| Cloud (historia de AWS) | [0:20:09](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=1209s) |
| Infraestructura global | [0:22:46](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=1366s) |
| Responsabilidad compartida | [0:30:53](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=1853s) |

## Resumen

Bloque teórico previo a la consola. Explica qué problema resuelve el cloud: en lugar de comprar y mantener
servidores calculando a ojo la capacidad futura, se alquilan recursos **bajo demanda** y se paga **por uso**.
Presenta los modelos de despliegue (privado, público, híbrido), los tipos de servicio (IaaS, PaaS, SaaS), las
tres bases del precio en AWS, la infraestructura global (regiones, zonas de disponibilidad, *edge locations*)
y el **modelo de responsabilidad compartida**. Todo esto sale mucho en el examen Cloud Practitioner.

El curso sigue este orden: fundamentos → primer contacto con AWS → IAM → EC2 y almacenamiento →
alta disponibilidad → S3 → bases de datos → serverless → costes.

## ¿Qué es el cloud computing?

Es el **suministro bajo demanda** de recursos informáticos (cómputo, almacenamiento, bases de datos,
aplicaciones...) a través de internet con **pago por uso**.

- Eliges el tipo y el tamaño exactos de lo que necesitas (CPU, RAM, disco) y lo tienes **en segundos**.
- AWS es dueño del hardware y lo mantiene; tú lo aprovisionas y lo usas desde una consola web (o la CLI/API).
- **IT tradicional:** servidores en tu oficina o CPD propio, personal dedicado a mantenerlos, y cada vez que la
  empresa crece hay que comprar más máquinas.
- Ejemplos de servicios cloud que usas a diario: Gmail, Dropbox (nació sobre AWS) y Netflix (corre en AWS).

### Modelos de despliegue

| Modelo | Qué es | Cuándo tiene sentido |
|--------|--------|----------------------|
| **Privado** | Infraestructura cloud usada por **una sola organización**, no expuesta al público (p. ej. Rackspace) | Control total, aplicaciones sensibles, necesidades muy específicas |
| **Público** | Recursos propiedad de un **proveedor** que los opera y los entrega por internet (AWS, Azure, Google Cloud) | La mayoría de casos |
| **Híbrido** | Parte de los servidores **en local** (*on-premises*) y parte en el cloud público, conectados | Migraciones graduales, datos sensibles que se quieren mantener en casa |

### Las 5 características del cloud computing

1. **Autoservicio bajo demanda:** aprovisionas recursos tú mismo, sin que nadie del proveedor intervenga.
2. **Amplio acceso a la red:** los recursos se usan por la red desde cualquier tipo de cliente.
3. **Multiinquilino y agrupación de recursos** (*multi-tenancy*): varios clientes comparten el mismo hardware
   físico, pero **aislados**: compartir un servidor no te da acceso a los datos de otra empresa.
4. **Elasticidad y escalabilidad rápidas:** adquieres y liberas recursos automáticamente según la demanda.
5. **Servicio medido:** el uso se mide y pagas exactamente por lo consumido.

> **Ejemplo de elasticidad del vídeo:** una app con 1 millón de usuarios de lunes a viernes necesita
> 100 servidores; el fin de semana baja a 200.000 usuarios y bastan 20. En el cloud el fin de semana solo
> pagas 20 servidores y el lunes vuelves a 100 (o a los que hagan falta).

### Las 6 ventajas del cloud (según AWS)

1. Cambiar **CapEx** (gasto de capital: comprar hardware) por **OpEx** (gasto operativo: pagar por uso).
   Reduce el coste total de propiedad (**TCO**).
2. Beneficiarse de **economías de escala masivas**: AWS compra y opera a una escala enorme y baja precios.
3. **Dejar de adivinar la capacidad**: escalas según el uso real medido.
4. **Aumentar la velocidad y la agilidad**: los recursos están a un clic.
5. **Dejar de gastar en mantener centros de datos** propios.
6. **Hacerse global en minutos** gracias a la infraestructura global de AWS.

### Problemas que resuelve

Flexibilidad (cambiar el tipo de recurso cuando haga falta), rentabilidad (pago por uso), escalabilidad
(más hardware o más nodos), elasticidad (subir y bajar según la demanda), alta disponibilidad y tolerancia
a fallos (varios centros de datos) y agilidad (desarrollar, probar y lanzar rápido).

## Tipos de cloud computing: IaaS, PaaS y SaaS

Cuanto más subes, menos gestionas tú:

| Capa | On-premises | IaaS | PaaS | SaaS |
|------|:-----------:|:----:|:----:|:----:|
| Aplicaciones | Tú | Tú | Tú | Proveedor |
| Datos | Tú | Tú | Tú | Proveedor |
| Runtime | Tú | Tú | Proveedor | Proveedor |
| Middleware | Tú | Tú | Proveedor | Proveedor |
| Sistema operativo | Tú | Tú | Proveedor | Proveedor |
| Virtualización | Tú | Proveedor | Proveedor | Proveedor |
| Servidores | Tú | Proveedor | Proveedor | Proveedor |
| Almacenamiento | Tú | Proveedor | Proveedor | Proveedor |
| Red | Tú | Proveedor | Proveedor | Proveedor |

- **IaaS** (infraestructura como servicio): te dan los bloques básicos (red, máquinas, almacenamiento).
  Máxima flexibilidad y lo más parecido a la IT tradicional. Ejemplos: **Amazon EC2**, GCP, Azure,
  Rackspace, DigitalOcean, Linode.
- **PaaS** (plataforma como servicio): solo despliegas y gestionas tu aplicación y tus datos.
  Ejemplos: **AWS Elastic Beanstalk**, Heroku, Google App Engine, Azure.
- **SaaS** (software como servicio): producto terminado que opera el proveedor; no gestionas nada.
  Ejemplos: **Amazon Rekognition** (visión artificial), Gmail, Dropbox, Zoom.

> **Nota de precisión:** a AWS Lambda se la suele clasificar aparte, como **FaaS** (función como servicio).
> El vídeo lo menciona más adelante al hablar de servicios regionales.

## Cómo se paga en AWS

Tres fundamentos del modelo de pago por uso:

1. **Cómputo:** pagas por el tiempo de computación (EC2, Lambda...).
2. **Almacenamiento:** pagas por los datos guardados (S3...).
3. **Transferencia de datos hacia FUERA del cloud.** La transferencia **hacia dentro es gratuita**.

## Un poco de historia (según el vídeo)

- **2002:** lanzamiento interno; Amazon ve que su infraestructura es un punto fuerte y decide venderla.
- **2004:** lanzamiento público de **SQS** (colas).
- **2006:** relanzamiento público con **SQS, S3 y EC2**.
- **2007:** llega a Europa.
- Clientes conocidos: Dropbox, Netflix, Airbnb, la NASA, McDonald's, 21st Century Fox, Activision.
- En 2025, según el vídeo, AWS ingresó unos 128.700 millones de dólares (≈ +20 % anual, impulsado por la IA),
  y Gartner la sitúa como líder de su *Magic Quadrant* por 15.º año consecutivo.
- Casos de uso: IT empresarial, copias de seguridad y almacenamiento, big data, webs, apps móviles y
  sociales, videojuegos.

## Infraestructura global

```
Región (p. ej. us-east-1, Norte de Virginia)
├── Zona de disponibilidad us-east-1a  →  uno o varios centros de datos
├── Zona de disponibilidad us-east-1b
└── Zona de disponibilidad us-east-1c
Edge locations / puntos de presencia  →  repartidos por ciudades de todo el mundo (CDN)
```

- **Región:** grupo de centros de datos en una zona geográfica con un nombre único (`us-east-1`,
  `eu-west-1`, `ap-southeast-2`...). La mayoría de servicios son **regionales**.
- **Zona de disponibilidad (AZ):** uno o varios centros de datos con alimentación, red y conectividad
  redundantes, **separados físicamente** de las otras AZ de la región (un desastre en una no afecta a otra)
  y unidos por redes de baja latencia. Normalmente 3 por región (máximo 6). Se nombran con una letra:
  `ap-southeast-2a`, `ap-southeast-2b`, `ap-southeast-2c`.
- **Edge location (punto de presencia):** ubicaciones de CloudFront que acercan el contenido a los usuarios
  finales con menos latencia. El vídeo da cifras de cientos de puntos en más de 40 países.

> **Nota de precisión:** las cifras de regiones, AZ y *edge locations* cambian a menudo (siempre al alza).
> Consulta las actuales en https://aws.amazon.com/about-aws/global-infrastructure/.

### Cómo elegir una región (pregunta típica de examen)

1. **Cumplimiento legal y gobernanza de datos:** los datos no salen de una región sin tu permiso explícito.
2. **Proximidad a los clientes:** menos latencia (clientes en Europa → región europea).
3. **Servicios disponibles:** no todos los servicios ni las novedades están en todas las regiones.
4. **Precio:** varía de una región a otra.

### Servicios globales y regionales

- **Globales** (el vídeo pide recordar estos cuatro): **IAM**, **Route 53** (DNS), **CloudFront** (CDN) y
  **WAF** (firewall de aplicaciones web).
- **Regionales:** la mayoría. Ejemplos: **EC2** (IaaS), **Elastic Beanstalk** (PaaS), **Lambda** (FaaS),
  **Rekognition** (SaaS).

> **Nota de precisión:** WAF es global solo cuando se asocia a CloudFront. Si lo usas con un ALB o una
> API Gateway, las reglas (*web ACLs*) son **regionales**. Hay más servicios de ámbito global además de los
> cuatro de la lista, por ejemplo AWS Organizations.

## Modelo de responsabilidad compartida

| El **cliente** es responsable de la seguridad **EN** el cloud | **AWS** es responsable de la seguridad **DEL** cloud |
|---|---|
| Los datos de sus clientes | El software de los servicios: cómputo, almacenamiento, bases de datos, redes |
| Gestión de accesos e identidades (IAM), aplicaciones y plataforma | El hardware y la infraestructura global: regiones, AZ, *edge locations* |
| Configuración del sistema operativo, la red y el firewall (grupos de seguridad) | |
| Cifrado en el cliente y en el servidor, y protección del tráfico de red | |

Ejemplo de la documentación oficial: **parches**. AWS parchea su infraestructura; el cliente parchea
**su sistema operativo invitado y sus aplicaciones** (por ejemplo, el Linux de una instancia EC2).

> La frontera cambia según el servicio: en EC2 el sistema operativo es tuyo; en un servicio gestionado
> como RDS el parcheo del sistema operativo lo hace AWS (apunte 07).

## Política de uso aceptable

AWS prohíbe usar sus servicios para contenido ilegal, dañino u ofensivo, para violar la seguridad de
otros, abusar de la red o enviar correo masivo no solicitado.
Referencia: https://aws.amazon.com/aup/

## Ejercicios

En [`01_fundamentos_cloud/ejercicios`](../01_fundamentos_cloud/ejercicios/):

1. Clasifica servicios en IaaS, PaaS, SaaS o FaaS.
2. Decide quién es responsable de cada tarea (cliente o AWS).
3. Calcula el ahorro de la elasticidad con el ejemplo de 100/20 servidores.
4. **Arregla este código:** una función que elige región ignorando los requisitos legales.
