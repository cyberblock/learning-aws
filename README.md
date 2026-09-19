# AWS desde cero (Guía de Aprendizaje)

Ruta para aprender Amazon Web Services apoyándote en el vídeo
[Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw)
de **Joan Amengual** ([canal de YouTube](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw)).
El vídeo es la referencia principal. Este repositorio reúne **apuntes propios**, los **comandos de la AWS CLI**
equivalentes a cada demo de la consola y **ejercicios con soluciones**.

> Son apuntes de estudio personales basados en el curso de Joan Amengual. No tienen relación oficial
> con el autor ni con Amazon Web Services. Para la explicación completa, mira el vídeo original.

## Objetivos
- Entender qué problema resuelve el cloud y cómo se organiza AWS (regiones, zonas, servicios).
- Crear y usar los servicios básicos: IAM, EC2, EBS, ELB, Auto Scaling, S3, RDS, DynamoDB y Lambda.
- Controlar el gasto desde el primer día (presupuestos, etiquetas, Cost Explorer).
- Tener una base sólida para el examen **AWS Certified Cloud Practitioner**.

---

## Estructura del repositorio

```
learning-aws/
├── README.md                   # esta guía
├── apuntes/                    # un apunte .md por sección del vídeo + índice (README.md)
├── NN_tema/                    # una carpeta por apunte
│   ├── README.md               #   qué hay en la carpeta y a qué tramo del vídeo corresponde
│   ├── *.sh / *.json / *.py    #   código del vídeo y comandos de la AWS CLI equivalentes
│   └── ejercicios/
│       ├── ejercicios_NN.py    #   enunciados + NotImplementedError para que los resuelvas
│       ├── soluciones_NN.py    #   soluciones
│       └── test_ejercicios_NN.py
└── tests/                      # validan scripts y JSON sin conectarse a AWS
```

## Preparación del entorno

1. **Cuenta de AWS** con un presupuesto y alertas por correo (apunte 02) antes de crear nada.
2. **Usuario IAM** para el día a día; no uses el usuario root (apunte 03).
3. **AWS CLI v2** (opcional, solo para los scripts `.sh`):
   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html.
   Configúrala con `aws configure` (o `aws configure sso`) y comprueba con `aws sts get-caller-identity`.
4. **Python 3.12 o superior** para los ejercicios:

```bash
python -m venv .venv
.venv/Scripts/activate           # Windows (Git Bash); en Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
```

> ⚠️ Los scripts `.sh` **crean recursos reales en AWS** y algunos pueden costar dinero. Léelos antes de
> ejecutarlos, cambia los valores de ejemplo y ejecuta siempre el bloque de limpieza del final.
> En este repositorio no se ha ejecutado ninguno contra AWS: los tests solo comprueban su sintaxis
> contra los modelos de la API (botocore).

## Cómo usar este repositorio

```bash
pytest                          # comprueba soluciones, scripts y JSON (no toca AWS)
pytest 04_ec2_ebs_efs           # solo un módulo
pytest 04_ec2_ebs_efs --mios    # comprueba TU versión de ejercicios_04.py
```

**Método de estudio recomendado para cada apunte:**
1. Mira el tramo del vídeo (el enlace del apunte salta al minuto exacto).
2. Lee el apunte en `apuntes/`: resumen, conceptos, errores típicos y notas de precisión.
3. Repite la demo en la consola y, si quieres, con los comandos de la CLI de la carpeta del módulo.
4. Resuelve `ejercicios/ejercicios_NN.py` sustituyendo cada `raise NotImplementedError`.
5. Compruébalo con `pytest NN_tema --mios` y compara con `soluciones_NN.py`.

---

## Progreso del curso

| # | Tema | Tramo del vídeo | Carpeta | Apuntes |
|:-:|------|-----------------|---------|---------|
| 01 | Fundamentos del cloud | [0:00:00](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=0s) | [01_fundamentos_cloud](01_fundamentos_cloud/) | [01](apuntes/01-fundamentos-cloud.md) |
| 02 | Primer contacto con AWS | [0:34:12](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s) | [02_primer_contacto](02_primer_contacto/) | [02](apuntes/02-primer-contacto-aws.md) |
| 03 | Seguridad e IAM | [0:53:05](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s) | [03_iam](03_iam/) | [03](apuntes/03-seguridad-iam.md) |
| 04 | Computación: EC2, EBS y EFS | [1:07:09](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s) | [04_ec2_ebs_efs](04_ec2_ebs_efs/) | [04](apuntes/04-ec2-ebs-efs.md) |
| 05 | Alta disponibilidad: ELB y Auto Scaling | [1:47:33](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s) | [05_alta_disponibilidad](05_alta_disponibilidad/) | [05](apuntes/05-alta-disponibilidad.md) |

**Leyenda de la ruta:** ✅ cubierto en el curso · 🟡 cubierto en parte · ⏳ pendiente (no está en el vídeo)

---

## Ruta de Aprendizaje

### 1. Fundamentos del cloud ✅
📺 Apunte 01 · 📁 `01_fundamentos_cloud`

Temas: qué es el cloud computing, modelos de despliegue, IaaS/PaaS/SaaS, modelo de precios,
infraestructura global, responsabilidad compartida.

Ejercicio: elige la región correcta para una app con datos que deben quedarse en la UE. → `ejercicios_01.py` (4)

### 2. Cuenta y control del gasto ✅
📺 Apunte 02 · 📁 `02_primer_contacto`

Temas: cuenta root, plan gratuito, presupuestos y alertas por correo, tour por la consola y selector de región.

Ejercicio: construye el JSON de un presupuesto mensual con alerta al 50 %. → `ejercicios_02.py` (4)

### 3. Identidad y acceso (IAM) ✅
📺 Apunte 03 · 📁 `03_iam`

Temas: usuario root frente a usuario IAM, grupos, políticas JSON, mínimo privilegio, alias de cuenta
y URL de inicio de sesión.

Ejercicio: decide si una política permite una acción concreta (con comodines). → `ejercicios_03.py` (4)

### 4. Computación (EC2) ✅
📺 Apunte 04 · 📁 `04_ec2_ebs_efs`

Temas: tipos de instancia, AMI, pares de claves, grupos de seguridad, *user data*, ciclo de vida
y cambio de IP pública al parar y arrancar.

Ejercicio: decide si un volumen se puede adjuntar a una instancia. → `ejercicios_04.py` (4)

### 5. Almacenamiento de instancias (EBS, Instance Store, EFS) ✅
📺 Apunte 04 · 📁 `04_ec2_ebs_efs`

Temas: volúmenes EBS y zonas de disponibilidad, *delete on termination*, instantáneas,
Instance Store efímero, EFS multizona y EFS-IA con política de ciclo de vida.

### 6. Alta disponibilidad y escalado (ELB + ASG) ✅
📺 Apunte 05 · 📁 `05_alta_disponibilidad`

Temas: escalado vertical y horizontal, elasticidad frente a agilidad, tipos de balanceadores
(ALB, NLB, GWLB), grupos de destino y comprobaciones de estado, grupos de autoescalado y
orden de limpieza de los recursos.

Ejercicio: reparte peticiones por turnos entre los destinos sanos. → `ejercicios_05.py` (4)

### 7. Almacenamiento de objetos (S3) ⏳
Temas: buckets, objetos y claves, acceso público, URLs prefirmadas.

### 8. Bases de datos (RDS, Aurora, DynamoDB) ⏳
Temas: relacional vs NoSQL, RDS gestionado, Aurora y Aurora Serverless, DynamoDB y DAX.

### 9. Serverless (Lambda) ⏳
Temas: serverless, precios de Lambda, eventos, logs en CloudWatch, rol de ejecución.

### 10. Costes y facturación ⏳
Temas: panel de facturación, etiquetas de asignación de costes, grupos de recursos, Cost Explorer.

### 11. Redes (VPC) ⏳
Temas: VPC, subredes públicas y privadas, tablas de rutas, Internet Gateway, NAT, *security groups* vs NACL.

### 12. DNS y entrega de contenido (Route 53, CloudFront) ⏳
Temas: zonas alojadas, registros, políticas de enrutamiento, distribuciones y caché en *edge locations*.

### 13. Infraestructura como código (CloudFormation) ⏳
Temas: plantillas, pilas (*stacks*), parámetros y salidas. Ejercicio: la demo de ALB + ASG como plantilla.

### 14. Monitorización y auditoría (CloudWatch, CloudTrail) ⏳
Temas: métricas, alarmas, logs, registro de llamadas a la API.

### 15. Mensajería y eventos (SQS, SNS, EventBridge) ⏳
Temas: colas, notificaciones, reglas programadas (cron *serverless*).

### 16. Preparar el Cloud Practitioner (CLF-C02) ⏳
Temas: guía oficial del examen, preguntas de práctica, repaso de las notas de precisión de los apuntes.

---

## Recursos Complementarios
- Documentación oficial de AWS: https://docs.aws.amazon.com/
- AWS Skill Builder (cursos gratuitos, incluido Cloud Practitioner Essentials): https://skillbuilder.aws/
- Guía del examen Cloud Practitioner (CLF-C02): https://aws.amazon.com/certification/certified-cloud-practitioner/
- Capa gratuita de AWS: https://aws.amazon.com/free/
- Calculadora de precios: https://calculator.aws/
- Servicios disponibles por región: https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
- Referencia de la AWS CLI: https://awscli.amazonaws.com/v2/documentation/api/latest/index.html
- Código del curso publicado por el autor: https://github.com/joaneeet7/codigo-aws-cloud-practitioner

## Créditos
- **Autor del curso:** Joan Amengual, ingeniero cloud e instructor de cloud y DevOps.
- **Canal:** https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw
- **Vídeo original:** [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw)
  (3:50:13, publicado el 16/04/2026). En la descripción del vídeo el autor enlaza sus recursos gratuitos.
- **Código del curso del autor:** https://github.com/joaneeet7/codigo-aws-cloud-practitioner (no se copia aquí; se enlaza).

Los apuntes, los scripts de la CLI y los ejercicios son material propio basado en ese curso. Todo el mérito
del contenido original es de su autor. Este repositorio no incluye el vídeo, su transcripción ni los
materiales descargables del curso.
