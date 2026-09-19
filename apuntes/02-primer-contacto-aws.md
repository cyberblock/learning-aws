# 02 · Primer contacto con AWS

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 18:53

**Tramo del vídeo:** 0:34:12 – 0:53:05

| Capítulo | Inicio |
|----------|--------|
| Primer contacto con AWS | [0:34:12](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2052s) |
| Creación cuentas AWS | [0:34:57](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2097s) |
| Cambios interfaz | [0:39:25](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2365s) |
| Presupuesto AWS | [0:41:24](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2484s) |
| Tour consola AWS | [0:45:22](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=2722s) |

**Código:** [`02_primer_contacto/`](../02_primer_contacto/): presupuesto en JSON y comandos de la CLI equivalentes.

## Resumen

Primeros pasos en la consola: crear la cuenta de AWS, configurar un **presupuesto con alertas** para no
llevarse sorpresas y dar una vuelta por la consola para entender las **regiones** y cómo se encuentran
los servicios. No hace falta aprenderse todos los servicios: basta con entender cómo se organizan.

## Crear la cuenta de AWS

1. Registro en la web oficial con el **correo del usuario root** (usuario raíz). Es la identidad más
   poderosa de la cuenta: guárdala bien.
2. **Nombre de la cuenta:** tu nombre si es para aprender, o algo como `aws-general` o `aws-prod` en una empresa.
3. Código de verificación enviado al correo y **contraseña**.
4. **Plan:** gratuito o de pago. Para el curso, el **plan gratuito**, con hasta **200 USD en créditos**.
5. Datos de contacto (nombre, organización si la hay, país, dirección).
6. **Método de pago obligatorio** aunque uses el plan gratuito (tarjeta o cuenta bancaria). AWS retiene
   1 USD para verificarlo y luego lo devuelve.
7. Verificación de identidad por **SMS** al móvil.
8. **Plan de soporte:** el básico, que es gratuito.
9. La cuenta tarda unos segundos en activarse y aparece el panel de la consola.

> **Nota de precisión:** desde julio de 2025 el plan gratuito da 100 USD al registrarte y hasta 100 USD más
> por completar actividades, y dura como máximo 6 meses (o hasta que gastes los créditos). Después hay que
> pasar al plan de pago o la cuenta se cierra. Comprueba las condiciones actuales en https://aws.amazon.com/free/.

> **Nota de precisión:** lo primero tras crear la cuenta es **activar MFA en el usuario root** (menú de la
> cuenta → Credenciales de seguridad). El vídeo no lo menciona, pero AWS lo considera imprescindible y ya lo
> exige a los usuarios root.

### Idioma y aspecto de la consola

**Unified Settings** (enlace al pie de la consola): idioma (el curso usa español) y modo claro u oscuro.

## La interfaz cambia a menudo

La consola se rediseña con frecuencia: botones, colores y opciones nuevas. Si lo que ves no coincide con el
vídeo, lo normal es que la **funcionalidad** siga siendo la misma y solo haya cambiado el aspecto. El autor se
compromete a regrabar las clases que dejen de poder seguirse.

## Presupuesto con alertas (AWS Budgets)

Pasos de la demo (buscador → **Budgets** / Presupuestos → Crear presupuesto):

1. **Personalización avanzada** → tipo **Presupuesto de costos**.
2. Nombre, periodo **mensual**, **recurrente**, importe **fijo**: por ejemplo **10 USD/mes**.
3. Ámbito: **todos los servicios** de la cuenta (se podría filtrar por servicios concretos).
4. **Alerta** por umbral: al llegar al **50 %** del presupuesto (5 USD), enviar un **correo**.
5. Acciones: ninguna (solo queremos el aviso).
6. Revisar y crear.

```json
{
  "BudgetName": "presupuesto-mensual",
  "BudgetLimit": { "Amount": "10", "Unit": "USD" },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

- ❌ Un presupuesto **no impide** gastar más: solo **avisa**.
- ✅ Es una buena práctica tenerlo desde el primer día. El autor avisa antes de cada práctica que pueda costar dinero.

> Las **acciones de presupuesto** (paso 5) sí pueden actuar: aplicar una política IAM o SCP que bloquee
> la creación de recursos, o detener instancias EC2 o RDS al superar un umbral.

## Tour por la consola

- **Selector de región** (arriba a la derecha, p. ej. *Norte de Virginia* = `us-east-1`). No hace falta estar
  físicamente en una región para usarla (el autor vive en España y usa `us-east-1`).
- Los precios y los servicios disponibles **cambian según la región**: compruébalo antes de elegirla.
- **Servicios:** menú por categorías (almacenamiento, análisis, administración de costos...) o el
  **buscador**, que además muestra características, blogs, documentación, artículos y Marketplace.
- **Visitados recientemente:** acceso rápido a los últimos servicios usados.
- **Servicio global vs regional en la consola:** en **Route 53** el selector muestra **Global** y no deja
  elegir región. En **EC2** vuelve a aparecer *Norte de Virginia*: es regional.
- ⚠️ Usa **siempre la misma región** durante el curso. Si creas una instancia en `us-east-1` y cambias a
  `eu-west-1`, no la verás (no se ha borrado, está en otra región).
- Widgets del inicio: **AWS Health**, **Costo y uso** (qué estás gastando) y **Trusted Advisor**
  (recomendaciones de costes, seguridad y rendimiento).
- Página de **servicios por región**:
  https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/

### Lo mismo con la AWS CLI

No aparece en el vídeo. Está en [`02_primer_contacto/cli-presupuesto.sh`](../02_primer_contacto/cli-presupuesto.sh)
y [`cli-regiones.sh`](../02_primer_contacto/cli-regiones.sh):

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws budgets create-budget --account-id "$ACCOUNT_ID" \
  --budget file://presupuesto.json \
  --notifications-with-subscribers file://notificaciones.json

aws ec2 describe-regions --query 'Regions[].RegionName' --output text
aws ec2 describe-availability-zones --region us-east-1 --query 'AvailabilityZones[].ZoneName'
```

## Ejercicios

En [`02_primer_contacto/ejercicios`](../02_primer_contacto/ejercicios/):

1. Convierte un umbral en porcentaje a dólares.
2. Construye el JSON del presupuesto mensual (se valida contra el modelo de la API de AWS Budgets).
3. Construye la notificación por correo del 50 %.
4. **Arregla este código:** una función que calcula qué alertas han saltado y compara dólares con porcentajes.
