# 09 · Costes y facturación

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12957s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 14:16

**Tramo del vídeo:** 3:35:57 – 3:50:13

| Capítulo | Inicio |
|----------|--------|
| Costes | [3:35:57](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12957s) |
| Dashboard facturación | [3:36:33](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=12993s) |
| Despedida | [3:49:04](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=13744s) |

**Código:** [`09_costes/`](../09_costes/): consultas de coste con la CLI y un CSV de ejemplo.

## Resumen

El pago por uso solo es una ventaja si sabes **qué estás gastando**. AWS da cuatro herramientas que van de
lo general a lo detallado: el **panel de facturación** (visión rápida), las **etiquetas de asignación de
costes** (repartir el gasto por proyecto o equipo), el **informe de costes y uso** (el dato en bruto) y
**Cost Explorer** (analizar, filtrar y prever). El presupuesto del apunte 02 sigue siendo la primera
defensa: avisa antes de que llegue la factura.

## Panel de facturación

En *Administración de facturación y costes*: resumen del gasto del mes, con gráficos que se pueden desglosar
**por servicio, por cuenta o por región**, acceso a las facturas y a las tendencias (en qué ha subido el
gasto). Sirve para la foto rápida, no para el análisis fino.

## Etiquetas de asignación de costes

Una **etiqueta** (*tag*) es un par clave-valor que se pone a casi cualquier recurso: instancias, volúmenes,
balanceadores, bases de datos, buckets, recursos creados por CloudFormation. Nombres habituales: `Name`,
`environment`, `team`, `owner`, `department`, `project`.

| Prefijo en los informes | Quién la crea |
|-------------------------|---------------|
| `aws:` | AWS, automáticamente (por ejemplo, `aws:cloudformation:stack-name`) |
| `user:` | Tú |

Con ellas se responde a "¿cuánto cuesta este proyecto?". Dos herramientas más:

- **Editor de etiquetas** (*Resource Groups & Tag Editor*): busca recursos por región y tipo, filtra por
  etiqueta —o por **falta** de etiqueta— y las aplica en bloque.
- **Grupos de recursos:** una colección de recursos que comparten etiquetas (o que vienen de una pila de
  CloudFormation), para verlos y gestionarlos juntos.

> **Nota de precisión.** Poner la etiqueta no basta: hay que **activarla** como etiqueta de asignación de
> costes en el panel de facturación, y solo aparece en los informes **desde ese momento** (no se aplica
> hacia atrás). Tarda hasta 24 horas en verse.

```bash
aws ce list-cost-allocation-tags --status Inactive
aws ce update-cost-allocation-tags-status --cost-allocation-tags-status TagKey=department,Status=Active
aws resourcegroupstaggingapi get-resources --tag-filters Key=department,Values=IT
```

## Informe de costes y uso (CUR)

El conjunto de datos **más completo** de facturación: desglose por servicio, cuenta, recurso y tiempo, con
muchísimas columnas. Se exporta a S3 y se analiza con **Athena, Redshift o QuickSight**. Es la opción cuando
Cost Explorer se queda corto.

## Cost Explorer

La herramienta de cabecera para entender el gasto:

- **Informes personalizados**, guardables en la biblioteca.
- Vista de alto nivel o **granularidad** mensual, diaria y **horaria**, útil para cazar picos.
- **Filtros** por servicio, cuenta vinculada, región, tipo de instancia o etiqueta.
- **Recomendaciones de planes de ahorro** según el uso real.
- **Previsión de hasta 12 meses** a partir del histórico, con margen de confianza.
- Descarga en CSV.

```bash
aws ce get-cost-and-usage --time-period Start=2026-04-01,End=2026-04-30 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
aws ce get-cost-forecast --time-period Start=2026-04-20,End=2026-05-01 \
  --metric UNBLENDED_COST --granularity MONTHLY
```

> **Nota de precisión.** Cost Explorer y las consultas de `aws ce` **se pagan por petición** (unos 0,01 USD
> cada una en la API; el primer uso de la interfaz activa el servicio). No es gratis del todo, aunque para
> una cuenta de estudio el importe es despreciable.

> **Nota de precisión.** Los datos de facturación llegan **con retraso** (horas, hasta un día). Un gasto que
> acabas de generar no aparece al momento: para reaccionar rápido, presupuestos y alarmas, no informes.

## Qué herramienta para qué

| Necesitas | Usa |
|-----------|-----|
| Que te avisen antes de gastar de más | **AWS Budgets** (apunte 02) |
| Ver de un vistazo el gasto del mes | Panel de facturación |
| Saber cuánto cuesta un proyecto o equipo | **Etiquetas** de asignación de costes |
| Analizar, filtrar y prever el gasto | **Cost Explorer** |
| El dato en bruto para analizarlo aparte | Informe de **costes y uso** exportado a S3 |

## Errores típicos

- Etiquetar recursos y no activar la etiqueta en facturación: no aparece en ningún informe.
- Empezar a etiquetar tarde: los informes no rellenan el pasado.
- Mirar solo el total del mes y no el desglose por servicio, que es donde se ve la fuga.
- Confiar en los informes para detectar un gasto que acaba de empezar, en lugar de un presupuesto.
- Dejar encendido lo caro (balanceadores, RDS, NAT) porque "no se ve" en la consola de EC2.

## Ejercicios

En [`09_costes/ejercicios`](../09_costes/ejercicios/):

1. Suma el coste de cada servicio a partir de las filas de un informe.
2. Saca los servicios que más gastan, ordenados.
3. Estima el gasto a fin de mes con el ritmo actual.
4. **Arregla este código:** una función que filtra las etiquetas de usuario y se cuela con las que genera
   AWS, además de no quitar el prefijo ni eliminar repetidos.
