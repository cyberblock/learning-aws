# 04 · Computación: EC2, EBS y EFS

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 40:24

**Tramo del vídeo:** 1:07:09 – 1:47:33

| Capítulo | Inicio |
|----------|--------|
| Computación (EC2) | [1:07:09](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4029s) |
| EC2 | [1:08:03](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4083s) |
| EC2 demo | [1:13:27](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4407s) |
| EBS | [1:28:54](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=5334s) |
| EBS demo | [1:35:20](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=5720s) |
| EFS | [1:41:12](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=6072s) |

**Código:** [`04_ec2_ebs_efs/`](../04_ec2_ebs_efs/): script de arranque y comandos de la CLI equivalentes.

## Resumen

**EC2** (*Elastic Compute Cloud*) es alquilar máquinas virtuales: eliges sistema operativo, CPU, RAM, disco,
red y cortafuegos, y arrancan en un par de minutos. Es IaaS puro y el servicio más presente en el examen.
Alrededor de EC2 van los tres tipos de almacenamiento: **EBS** (disco de red, una instancia a la vez, atado a
una zona), **Instance Store** (disco físico del servidor, rapidísimo pero efímero) y **EFS** (sistema de
archivos compartido por muchas instancias y varias zonas).

## Qué ofrece EC2

Cuatro capacidades que se apoyan unas en otras:

| Pieza | Para qué |
|-------|----------|
| **EC2** | Las máquinas virtuales (instancias) |
| **EBS** | Los discos de red donde persisten los datos |
| **ELB** | Repartir la carga entre varias instancias (apunte 05) |
| **Auto Scaling** | Añadir o quitar instancias según la demanda (apunte 05) |

Lo que se elige al crear una instancia: sistema operativo (Linux, Windows, macOS), potencia (CPU y RAM),
almacenamiento (EBS/EFS por red o Instance Store físico), red (velocidad de la tarjeta, IP pública),
**grupo de seguridad** (el cortafuegos) y **datos de usuario** (el script de arranque).

### Datos de usuario (*user data*)

Script que se ejecuta **una sola vez, en el primer arranque**, y **como root**. Sirve para dejar la máquina
lista sin tocarla a mano: actualizar el sistema, instalar software, descargar archivos. El de la demo está
en [`04_ec2_ebs_efs/user-data.sh`](../04_ec2_ebs_efs/user-data.sh):

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hola mundo desde $(hostname -f)</h1>" > /var/www/html/index.html
```

> **Nota de precisión.** Solo se ejecuta en el primer arranque, no en cada `start`. Si necesitas que algo
> corra en todos los arranques, ponlo en un servicio de systemd. Y ojo: los datos de usuario se pueden
> consultar desde la propia instancia, así que **nunca** metas contraseñas ni claves ahí.

## Lanzar la instancia (demo)

1. **Nombre** y etiquetas opcionales.
2. **AMI** (*Amazon Machine Image*): la plantilla del disco. La demo usa **Amazon Linux**, incluida en la
   capa gratuita. Hay AMIs de Ubuntu, Windows, Red Hat, macOS, del Marketplace o propias.
3. **Tipo de instancia:** la combinación de CPU y RAM. La demo usa **`t2.micro`**, la de la capa gratuita.
   Qué tipos hay y a qué precio **depende de la región**.
4. **Par de claves** para entrar por SSH: algoritmo RSA y formato `.pem` (Linux, macOS, Windows 10+) o
   `.ppk` (PuTTY en Windows antiguos). La clave **privada se descarga una única vez**.
5. **Red y grupo de seguridad:** la consola crea uno tipo `launch-wizard-N`. Hay que marcar *permitir
   tráfico HTTP desde internet* para que la web responda.
6. **Almacenamiento** y, en *detalles avanzados*, los **datos de usuario**.
7. Lanzar. La instancia pasa a *running* en unos 30 segundos.

La página se abre en `http://<ip-pública>`. Si el navegador pone `https://` por su cuenta, **no carga**:
solo está abierto el puerto 80. Es el fallo de la demo y el error típico del principio.

> **Nota de precisión.** Las instancias son **regionales**: si cambias de región en la consola, no las ves.
> No se han borrado, están en la otra región. Y `t2.micro` solo es gratis dentro de los límites de la capa
> gratuita (horas al mes, durante 12 meses).

### Ciclo de vida

| Acción | Qué pasa | ¿Se paga? |
|--------|----------|-----------|
| *Start* / *Stop* | La instancia se apaga y se puede volver a arrancar | El cómputo no; **el disco EBS sí** |
| *Reboot* | Reinicio; conserva la IP pública | Sí |
| *Terminate* | Se destruye, no hay vuelta atrás | No (salvo volúmenes que sobrevivan) |

> **Nota de precisión.** Al parar y volver a arrancar, la **IP pública cambia**. Eso lo enseña el vídeo. Lo
> que no dice es la solución: una **IP elástica** (fija) o, mejor, poner un **balanceador o un nombre DNS**
> delante. Con un *reboot* la IP no cambia; con *stop* + *start*, sí.

## EBS · discos de red

- *Elastic Block Store*: un **disco de red** que se conecta a una instancia mientras esta corre. La analogía
  del vídeo es buena: un **pendrive de red**.
- Los datos **persisten** aunque la instancia se termine (si así se configura).
- **Una instancia a la vez** (lo que entra en el examen de Cloud Practitioner). Al revés sí: una instancia
  puede tener **varios** volúmenes.
- Está **atado a una zona de disponibilidad**: un volumen de `us-east-1a` no se adjunta a una instancia de
  `us-east-1b`. Para moverlo: **instantánea** (*snapshot*) y restaurar en la otra zona.
- Puede existir **sin estar adjunto** a ninguna instancia.
- **Capacidad aprovisionada:** eliges GiB e IOPS y **pagas por lo aprovisionado, lo uses o no**. Se puede
  ampliar en caliente.

### Borrar al terminar (*delete on termination*)

| Volumen | Valor por defecto |
|---------|-------------------|
| **Raíz** (el del sistema) | **Sí** se borra al terminar la instancia |
| Volúmenes **añadidos** | **No** se borran |

Se cambia al crear la instancia (*configurar almacenamiento → avanzado*) o después, desde la consola o la
CLI. Caso típico: desmarcarlo en el volumen raíz para conservar los datos aunque la instancia desaparezca.
Es una pregunta habitual del examen.

```bash
aws ec2 modify-instance-attribute --instance-id i-0123456789abcdef0 \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"DeleteOnTermination":false}}]'
```

> **Nota de precisión.** Un volumen sin adjuntar **sigue costando dinero**. Es una de las fuentes de gasto
> olvidado más frecuentes: se terminan instancias y quedan volúmenes e instantáneas huérfanos.

> **Nota de precisión.** Que solo se adjunte a una instancia es la regla de Cloud Practitioner. EBS
> Multi-Attach existe para volúmenes `io1`/`io2` en la misma zona, pero no entra en este examen. Y cifra los
> volúmenes: en la demo se deja sin cifrar y en una cuenta real conviene activarlo por defecto.

## Instance Store · disco físico

Almacenamiento del **hardware del propio servidor**. Es el más rápido, pero es **efímero**: si la instancia
se para o se termina, los datos desaparecen. Sirve para cachés, ficheros temporales o *scratch*; nunca para
lo que no puedas perder.

## EFS · sistema de archivos compartido

- *Elastic File System*: un **NFS gestionado** que se monta a la vez en **muchas instancias Linux** y en
  **varias zonas de disponibilidad** (un punto de montaje por zona).
- Alta disponibilidad, **crece y decrece solo** (sin aprovisionar capacidad) y se paga por uso.
- Es **más caro** que EBS por GiB.
- Lleva **grupo de seguridad**, igual que una instancia.

### EBS frente a EFS

| | EBS | EFS |
|---|-----|-----|
| Qué es | Disco de bloques | Sistema de archivos (NFS) |
| Instancias a la vez | Una | Muchas |
| Zonas | Una sola | Varias |
| Capacidad | Aprovisionada (pagas lo reservado) | Elástica (pagas lo usado) |
| Mover datos entre zonas | Instantánea + restaurar | No hace falta |
| Sistema operativo | Cualquiera | Linux |

### EFS-IA (*Infrequent Access*)

Clase de almacenamiento para archivos a los que casi no se accede: hasta un **92 % más barato** que EFS
estándar. Con una **política de ciclo de vida**, EFS mueve solo los archivos que llevan N días sin accesos
(1, 7, 14, 30, 60, 90, 180, 270 o 365). Es **transparente**: las aplicaciones no se enteran.

```bash
aws efs put-lifecycle-configuration --file-system-id fs-0123456789abcdef0 \
  --lifecycle-policies '[{"TransitionToIA":"AFTER_60_DAYS"},{"TransitionToPrimaryStorageClass":"AFTER_1_ACCESS"}]'
```

## Errores típicos

- Entrar por `https://` cuando solo está abierto el puerto 80.
- Buscar la instancia en otra región y pensar que se ha perdido.
- Guardar la IP pública en algún sitio y pararla luego: al arrancar de nuevo, otra IP.
- Crear el volumen EBS en una zona distinta a la de la instancia: no se puede adjuntar.
- Terminar instancias y dejar volúmenes e instantáneas sueltos pagando.
- Usar Instance Store para datos que importan.

## Ejercicios

En [`04_ec2_ebs_efs/ejercicios`](../04_ec2_ebs_efs/ejercicios/):

1. Coste mensual de un volumen EBS (se paga lo aprovisionado, no lo usado).
2. Decide si un volumen se puede adjuntar a una instancia (zona y ocupación).
3. Construye la política de ciclo de vida de EFS hacia EFS-IA.
4. **Arregla este código:** una función que dice qué volúmenes sobreviven al terminar la instancia e
   invierte la condición y los valores por defecto de raíz y no raíz.
