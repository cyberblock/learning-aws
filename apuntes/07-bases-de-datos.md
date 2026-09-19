# 07 · Bases de datos: RDS, Aurora y DynamoDB

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9689s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 37:27

**Tramo del vídeo:** 2:41:29 – 3:18:56

| Capítulo | Inicio |
|----------|--------|
| Bases de datos | [2:41:29](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9689s) |
| Intro bases de datos | [2:42:07](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=9727s) |
| RDS Aurora | [2:48:07](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=10087s) |
| RDS demo | [2:56:10](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=10570s) |
| DynamoDB | [3:09:23](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11363s) |
| DynamoDB demo | [3:13:12](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=11592s) |

**Código:** [`07_bases_datos/`](../07_bases_datos/): comandos de la CLI para RDS y DynamoDB.

## Resumen

Guardar archivos en disco (EBS, EFS, S3) no es lo mismo que guardar **datos**. Una base de datos permite
estructurarlos, indexarlos y relacionarlos, y está optimizada para consultarlos. En AWS hay dos familias:
**relacionales** (RDS y Aurora, con SQL y esquema fijo) y **no relacionales** (DynamoDB, clave-valor, con
esquema libre). La palabra clave en todas ellas es **gestionado**: AWS pone la infraestructura, las copias,
los parches y la monitorización; tú pones los datos.

## Relacional frente a no relacional

| | Relacional (SQL) | No relacional (NoSQL) |
|---|------------------|------------------------|
| Forma | Tablas con filas y columnas, como una hoja de cálculo | Clave-valor, documentos, grafos, en memoria |
| Esquema | Fijo, definido de antemano | Flexible, cambia con el tiempo |
| Relaciones | Sí, por claves entre tablas | No; los datos se guardan juntos |
| Consultas | SQL con `JOIN` | Por clave, sin uniones entre tablas |
| Escalado | Sobre todo vertical | Horizontal, en clústeres distribuidos |
| Ejemplo de dato | Tabla `estudiantes` + tabla `departamentos` | Documento JSON anidado |

> **Truco de examen.** Si el enunciado menciona **JSON**, datos anidados o campos que cambian, la respuesta
> es una base de datos **no relacional**.

### Qué aporta que sea gestionada

Aprovisionamiento automático, parcheo del sistema operativo, copias de seguridad continuas con
**restauración a un punto en el tiempo**, paneles de monitorización, réplicas de lectura, despliegue
**multi-AZ**, ventanas de mantenimiento y escalado. Todo eso lo puedes montar tú en una instancia EC2, pero
entonces la resiliencia, las copias, los parches y la alta disponibilidad son tuyos.

## Amazon RDS

Servicio de bases de datos **relacionales** gestionado. Motores disponibles: **MySQL, PostgreSQL, MariaDB,
Oracle, SQL Server, IBM Db2** y **Amazon Aurora**.

- El almacenamiento va sobre **EBS** y puede crecer solo hasta un tope que tú fijas.
- **No hay acceso por SSH**: AWS abstrae la máquina. Te conectas por el motor (`mysql`, `psql`...).
- Patrón habitual: las instancias EC2 detrás de un balanceador hablan con RDS **por la red privada**. La
  base de datos **no se expone a internet**.

### Demo: crear la instancia MySQL

1. **Método**: creación estándar (la sencilla deja casi todo prefijado).
2. **Motor** y **versión**. La versión importa: con versiones sin soporte, el precio sube.
3. **Plantilla**: producción, desarrollo o **capa gratuita**. Al elegir capa gratuita se desactiva el
   despliegue multi-AZ.
4. **Credenciales**: usuario maestro y contraseña, o gestión con **Secrets Manager**.
5. **Clase de instancia** (`db.t4g.micro` en la capa gratuita) y **almacenamiento** (20 GB gp2, con escalado
   automático hasta 1000 GB).
6. **Conectividad**: VPC, **acceso público: no**, grupo de seguridad propio y **puerto 3306**.
7. **Autenticación**: por contraseña, o contraseña + IAM, o Kerberos.

Al terminar, la ficha de la base de datos da lo que necesita la aplicación: **punto de enlace (endpoint) y
puerto**, además de red, seguridad, métricas de CloudWatch, eventos y registros.

```bash
aws rds create-db-instance --db-instance-identifier demo-mysql \
  --engine mysql --db-instance-class db.t4g.micro \
  --allocated-storage 20 --master-username admin --master-user-password "$PASSWORD" \
  --no-publicly-accessible --backup-retention-period 7
aws rds describe-db-instances --db-instance-identifier demo-mysql \
  --query 'DBInstances[0].Endpoint'
```

### Instantáneas (*snapshots*)

Una instantánea de RDS se puede **compartir** con otra cuenta (privada o públicamente), **copiar a otra
región** y **restaurar** allí, o **exportar a S3**. Es la vía para mover una base de datos de región o para
dar una copia a otro equipo.

> **Nota de precisión.** La capa gratuita de RDS cubre **750 horas al mes** de una instancia pequeña en
> **una sola zona**, durante 12 meses. En cuanto activas multi-AZ o subes de clase, se paga. Y una instancia
> **detenida** se reactiva sola a los 7 días: parar no es lo mismo que borrar.

> **Nota de precisión.** Al borrar, la consola ofrece conservar copias automáticas e instantánea final. Si
> las conservas, siguen ocupando y **siguen costando** aunque la base de datos ya no exista.

## Amazon Aurora

Base de datos relacional **propia de AWS**, no de código abierto, **compatible con MySQL y PostgreSQL**
(por eso migrar es sencillo). Diseñada para la nube:

- Mucho más rendimiento que el motor estándar, a cambio de **más precio**.
- El almacenamiento **crece solo en bloques de 10 GB**, hasta 128 TiB.
- **No está en la capa gratuita**.

### Aurora Serverless

Da un paso más: **no se definen instancias, ni tamaños, ni capacidad**. La aplicación se conecta a una capa
de **proxy** y AWS añade o quita capacidad por debajo según el uso real, sin mover los datos (el
almacenamiento está separado y es compartido). Se paga **por uso**, por segundo.

Ideal para cargas **intermitentes o impredecibles**; para una carga constante y alta suele salir más barata
una instancia normal.

> **Nota de precisión.** En el vídeo se menciona un máximo de 256 TB de almacenamiento en Aurora. El límite
> vigente es de **128 TiB** por clúster. Son cifras que AWS cambia: consúltalas en la documentación antes de
> diseñar nada.

## Amazon DynamoDB

Base de datos **NoSQL clave-valor**, **sin servidor** y totalmente gestionada.

- Replicada en **tres zonas de disponibilidad**.
- Escala a cargas enormes: millones de peticiones por segundo.
- Latencia de **milisegundo** constante.
- Integrada con **IAM** para permisos.
- Clases de tabla **estándar** e **infrecuente** (como las clases de almacenamiento).

### Tablas, claves y elementos

- La **clave de partición** forma la clave principal; puede haber además una **clave de ordenación**.
- Los tipos de la clave son **binario, cadena o número**.
- Solo se declara el esquema de la clave: **cada elemento puede tener atributos distintos**. Un usuario sin
  apellido simplemente no tiene ese atributo.
- Los valores se escriben con su tipo:

```json
{
  "user_id": {"N": "1234"},
  "nombre": {"S": "Joan"},
  "activo": {"BOOL": true}
}
```

```bash
aws dynamodb create-table --table-name demo-usuarios \
  --attribute-definitions AttributeName=user_id,AttributeType=N \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
aws dynamodb put-item --table-name demo-usuarios --item file://item-usuario.json
```

> **Nota de precisión.** En el vídeo se dice que el nombre de la tabla admite de 3 a 25 caracteres. El
> límite real es de **3 a 255**, con letras, números, `_`, `-` y `.`.

### DAX (*DynamoDB Accelerator*)

Caché en memoria gestionada **solo para DynamoDB**. Pone la latencia en **microsegundos** (hasta 10 veces
más rápido) sin cambiar el código.

| | DAX | ElastiCache |
|---|-----|-------------|
| Para qué | Solo DynamoDB | Cualquier base de datos (por ejemplo, RDS) |
| Uso típico | Acelerar lecturas de tablas | Caché de consultas o de sesiones |

En el examen: "acelerar el acceso a datos de DynamoDB" → **DAX**.

## Errores típicos

- Exponer la base de datos a internet en lugar de dejarla en la red privada.
- Esperar acceso SSH a RDS.
- Activar multi-AZ "por probar" estando en la capa gratuita.
- Borrar la instancia y dejar copias e instantáneas pagando.
- Elegir una base de datos relacional para datos JSON que cambian de forma constante.
- Responder ElastiCache cuando el enunciado habla de acelerar DynamoDB.

## Ejercicios

En [`07_bases_datos/ejercicios`](../07_bases_datos/ejercicios/):

1. Decide si un caso pide base de datos relacional o no relacional.
2. Convierte un diccionario de Python al formato de atributos de DynamoDB.
3. Valida el nombre de una tabla de DynamoDB.
4. **Arregla este código:** una función que saca los atributos de una tabla NoSQL mirando solo el primer
   elemento, como si todos compartieran esquema.
