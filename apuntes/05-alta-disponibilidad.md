# 05 · Alta disponibilidad: ELB y Auto Scaling

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 39:59

**Tramo del vídeo:** 1:47:33 – 2:27:32

| Capítulo | Inicio |
|----------|--------|
| Alta disponibilidad | [1:47:33](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6453s) |
| Disponibilidad, elasticidad y escalabilidad | [1:48:30](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6510s) |
| Load Balancer | [1:57:01](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=7021s) |
| ALB demo | [2:02:42](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=7362s) |
| Auto Scaling Group | [2:11:08](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=7868s) |
| Auto Scaling demo | [2:16:11](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8171s) |
| Limpieza de recursos | [2:26:00](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=8760s) |

**Código:** [`05_alta_disponibilidad/`](../05_alta_disponibilidad/): comandos de la CLI equivalentes al ALB y al grupo de autoescalado.

## Resumen

No basta con que la aplicación funcione: tiene que **seguir funcionando cuando algo falla**. Dos ideas
sostienen eso en AWS. El **balanceador de carga** (ELB) reparte las peticiones entre varias instancias, las
vigila y deja de mandar tráfico a la que se cae. El **grupo de autoescalado** (ASG) mantiene el número de
instancias que toca en cada momento y repone las que mueren. Juntos dan **elasticidad** (ajustarse a la
demanda) y **alta disponibilidad** (sobrevivir a la caída de una zona).

## Escalabilidad, elasticidad y agilidad

| Concepto | Qué es | Ejemplo |
|----------|--------|---------|
| **Escalado vertical** (*scale up/down*) | Instancia **más grande** | `t2.nano` → `t2.large` |
| **Escalado horizontal** (*scale out/in*) | **Más instancias** de lo mismo | 1 → 6 instancias |
| **Alta disponibilidad** | Lo mismo corriendo en **≥ 2 zonas de disponibilidad** | ASG y ALB *multi-AZ* |
| **Elasticidad** | El escalado **automático** según la carga | El ASG añade instancias el fin de semana |
| **Agilidad** | Tener recursos nuevos **en minutos**, no en semanas | Lanzar una instancia con un clic |

- El escalado **vertical** es típico de sistemas no distribuidos, como una base de datos. Tiene un techo: el
  límite del hardware.
- El escalado **horizontal** implica sistemas distribuidos y es lo natural en aplicaciones web.
- La **alta disponibilidad** va de la mano del escalado horizontal: el objetivo es sobrevivir a la pérdida
  de un centro de datos entero.

> **Nota de precisión.** *Agilidad* es un **distractor** en el examen: suena a elasticidad, pero no lo es.
> Elasticidad = ajustarse solo a la carga. Agilidad = velocidad para disponer de recursos.

> **Nota de precisión.** Alta disponibilidad no es lo mismo que tolerancia a desastres. Varias zonas
> protegen frente a la caída de un centro de datos; frente a la caída de una **región** entera hace falta
> replicar en otra región.

## Balanceadores de carga (ELB)

Un balanceador es un servidor que recibe el tráfico de internet y lo reenvía a varias instancias. La
respuesta vuelve por el mismo camino. Qué aporta:

- Reparte la carga entre varias instancias.
- Expone **un único nombre DNS** para toda la aplicación.
- Hace **comprobaciones de estado** y saca del reparto a la instancia que no responde.
- Termina el **SSL/HTTPS**.
- Da **alta disponibilidad entre zonas**.

**Elastic Load Balancing** es la versión gestionada por AWS: se encarga del mantenimiento, las
actualizaciones y la disponibilidad, y se configura con pocos ajustes. Montar el balanceador a mano dentro
de una instancia es posible, pero sale mucho más caro en trabajo.

| Tipo | Capa | Protocolos | Para qué |
|------|------|------------|----------|
| **ALB** (*Application*) | 7 | HTTP, HTTPS, gRPC | Web. Enrutado por ruta o por cabecera. DNS estático |
| **NLB** (*Network*) | 4 | TCP, UDP | Rendimiento extremo, millones de peticiones/s. **IP estática** |
| **GWLB** (*Gateway*) | 3 | GENEVE sobre IP | Pasar el tráfico por cortafuegos o IDS de terceros |
| *Classic* (CLB) | 4 y 7 | — | Generación anterior, retirado en 2023 |

### Demo del ALB

1. Dos instancias con el mismo script de arranque (`user-data.sh` del módulo 04). Cada una responde con su
   propio nombre, así se ve a cuál ha ido la petición.
2. **Grupo de seguridad** del ALB: HTTP (puerto 80) desde cualquier origen.
3. **Grupo de destino** (*target group*): tipo *instancias* (también valen IPs, funciones Lambda u otros
   ALB), protocolo HTTP:80 y **ruta de comprobación de estado** (`/` por defecto).
4. **Agente de escucha** (*listener*) en el puerto 80 que reenvía a ese grupo de destino.
5. Mapear el ALB a **todas las zonas de disponibilidad** de la región.
6. Al recargar el DNS del balanceador, las respuestas **van alternando** entre las dos instancias.
7. Si se **para** una instancia, el grupo de destino la marca `unhealthy` y todo el tráfico va a la otra. Al
   arrancarla de nuevo vuelve sola al reparto: no hay que reconfigurar nada.

```bash
aws elbv2 create-target-group --name demo-tg-alb --protocol HTTP --port 80 \
  --vpc-id vpc-0123456789abcdef0 --target-type instance --health-check-path /
aws elbv2 create-listener --load-balancer-arn "$ALB" --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn="$DESTINO"
aws elbv2 describe-target-health --target-group-arn "$DESTINO"
```

> **Nota de precisión.** El ALB da un **nombre DNS**, no una IP fija: sus direcciones cambian. Nunca apuntes
> a la IP de un ALB; usa el DNS (o un alias de Route 53). El que sí ofrece IP estática es el NLB.

> **Nota de precisión.** El grupo de seguridad de las **instancias** debería aceptar el puerto 80 solo desde
> el grupo de seguridad del **ALB**, no desde internet. En la demo quedan abiertas a todo el mundo.

## Grupos de autoescalado (ASG)

La carga de una web cambia con la hora y el día. El ASG ajusta el número de instancias solo:

- **Añade** instancias cuando sube la carga y las **quita** cuando baja.
- Respeta un **mínimo** y un **máximo**, y mantiene la **capacidad deseada**.
- **Registra** las instancias nuevas en el grupo de destino del balanceador.
- **Reemplaza** las instancias en mal estado.
- Ahorra dinero: solo corre la capacidad necesaria.

| Parámetro | En la demo | Qué significa |
|-----------|-----------|----------------|
| Mínimo | 1 | Nunca baja de aquí |
| Capacidad deseada | 2 | Lo que mantiene ahora mismo |
| Máximo | 4 | Nunca sube de aquí |

### Demo del ASG

1. **Plantilla de lanzamiento** (*launch template*), versionada: AMI, tipo de instancia (`t3.micro`), grupo
   de seguridad y **datos de usuario**. Sustituye a las antiguas configuraciones de lanzamiento.
2. Red: la VPC y **todas las subredes** disponibles, para repartir por zonas.
3. **Asociar al grupo de destino** del ALB y activar las **comprobaciones de estado de ELB**: así el ASG usa
   la salud que ve el balanceador, no solo la de EC2.
4. Tamaño del grupo: mínimo 1, deseada 2, máximo 4. Políticas de escalado: en el vídeo, ninguna.
5. Al crearlo, aparecen **dos instancias** sin tocar nada.
6. Prueba: se **terminan las dos a la vez**. El ASG las detecta como no sanas y **lanza dos nuevas** para
   volver a la capacidad deseada. El balanceador recupera el servicio solo.

```bash
aws autoscaling create-auto-scaling-group --auto-scaling-group-name demo-asg \
  --launch-template LaunchTemplateName=demo-template-launch,Version='$Latest' \
  --min-size 1 --desired-capacity 2 --max-size 4 \
  --vpc-zone-identifier subnet-aaa,subnet-bbb \
  --target-group-arns "$DESTINO" --health-check-type ELB
```

> **Nota de precisión.** Sin política de escalado, el ASG **no escala**: solo mantiene la capacidad deseada
> y repone lo que muere. Para que reaccione a la carga hay que añadir una política; la más sencilla es el
> **seguimiento de objetivo** (por ejemplo, CPU media al 50 %), que está en
> [`cli-asg.sh`](../05_alta_disponibilidad/cli-asg.sh).

> **Nota de precisión.** `--health-check-grace-period` importa: es el tiempo que el ASG espera antes de
> juzgar a una instancia recién lanzada. Si el arranque tarda más que ese margen, el grupo entra en un bucle
> de matar y relanzar instancias que nunca llegan a estar listas.

## Limpieza de recursos

El orden no es opcional:

1. **Grupo de autoescalado** primero. Si terminas las instancias antes, las vuelve a lanzar.
2. **Balanceador de carga**.
3. **Grupo de destino** (no cuesta dinero, pero no se borra hasta que el ALB desaparece del todo).
4. **Instancias** que queden sueltas.

```bash
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name demo-asg --force-delete
aws elbv2 delete-load-balancer --load-balancer-arn "$ALB"
aws elbv2 delete-target-group --target-group-arn "$DESTINO"
```

## Errores típicos

- Terminar instancias con el ASG vivo y no entender por qué reaparecen.
- Dejar un ALB encendido: se paga por hora aunque no reciba ni una petición.
- Poner el ASG en una sola zona: deja de haber alta disponibilidad.
- Confundir elasticidad con agilidad en el examen.
- Esperar que el ASG escale sin haberle puesto ninguna política.

## Ejercicios

En [`05_alta_disponibilidad/ejercicios`](../05_alta_disponibilidad/ejercicios/):

1. Di si un cambio es escalado vertical, horizontal, mixto o ninguno.
2. Calcula la capacidad final de un ASG respetando mínimo y máximo.
3. Reparte peticiones por turnos entre los destinos sanos del balanceador.
4. **Arregla este código:** una función que decide si hay alta disponibilidad contando instancias en lugar
   de zonas de disponibilidad con instancias sanas.
