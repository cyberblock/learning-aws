# Apuntes · Curso de AWS (Joan Amengual)

Apuntes de estudio personales del vídeo
[Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw)
de [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw).
Es un único vídeo de 3:50:13. Cada apunte corresponde a una de sus secciones y enlaza al minuto exacto.
Son resúmenes con explicaciones propias. Para la explicación completa, mira el vídeo original.

> Las **notas de precisión** marcadas en algunos apuntes son aclaraciones o correcciones técnicas añadidas que no aparecen en el vídeo.

## Índice

### Módulo A · Fundamentos
| # | Tema | Duración |
|---|------|----------|
| 01 | [Fundamentos del cloud](01-fundamentos-cloud.md) | 34:12 |

### Módulo B · Primer contacto
| # | Tema | Duración |
|---|------|----------|
| 02 | [Primer contacto con AWS](02-primer-contacto-aws.md) | 18:53 |

### Módulo C · Seguridad
| # | Tema | Duración |
|---|------|----------|
| 03 | [Seguridad e IAM](03-seguridad-iam.md) | 14:04 |

### Módulo D · Computación
| # | Tema | Duración |
|---|------|----------|
| 04 | [Computación: EC2, EBS y EFS](04-ec2-ebs-efs.md) | 40:24 |

## Chuleta rápida

### Conceptos
| Concepto | En una línea |
|----------|--------------|
| IaaS / PaaS / SaaS / FaaS | EC2 / Elastic Beanstalk / Rekognition, Gmail / Lambda |
| Precio | Cómputo + almacenamiento + transferencia **saliente** (la entrante es gratis) |
| Región → AZ → CPD | `us-east-1` → `us-east-1a` → uno o varios centros de datos |
| Elegir región | Legal → latencia → servicios disponibles → precio |
| Servicios globales | IAM, Route 53, CloudFront, WAF (con CloudFront) |
| Responsabilidad compartida | AWS: seguridad **del** cloud · Cliente: seguridad **en** el cloud |
| Usuario root | El del registro. No se usa para el día a día: crea un usuario IAM |
| Presupuesto | AWS Budgets, servicio global. Alerta por correo antes de gastar de más |
| Coste real vs previsto | `ACTUAL` = ya gastado · `FORECASTED` = previsión de fin de mes |
| Región en la consola | Selector arriba a la derecha. Si cambias de región, no ves los recursos de la otra |
| IAM | Servicio **global**: quién puede hacer qué. Usuarios, grupos, políticas JSON |
| Grupos | Solo contienen usuarios, nunca otros grupos. Un usuario puede estar en varios |
| Política | `Version` (siempre `2012-10-17`) + `Statement` con `Effect`, `Action`, `Resource` |
| Evaluación | Todo denegado por defecto · un `Deny` explícito gana a cualquier `Allow` |
| Mínimo privilegio | Solo los permisos necesarios. `AdministratorAccess` no es para el día a día |
| Alias de cuenta | `https://<alias>.signin.aws.amazon.com/console`. Único en todo AWS, uno por cuenta |
| EC2 | Máquinas virtuales de alquiler. Servicio **regional** |
| AMI | La plantilla del disco. `t2.micro` es el tipo de la capa gratuita |
| User data | Script de arranque. Se ejecuta **una vez**, como root |
| Stop + start | La **IP pública cambia**. Un *reboot* la conserva |
| EBS | Disco de red. **Una** instancia a la vez, atado a **una** zona. Pagas lo aprovisionado |
| Delete on termination | Volumen raíz: **sí** por defecto · volúmenes añadidos: **no** |
| Instance Store | Disco físico del servidor: rapidísimo y **efímero** |
| EFS | NFS gestionado: **muchas** instancias Linux y **varias** zonas. Caro, pago por uso |
| EFS-IA | Hasta un 92 % más barato para lo que no se toca (política de ciclo de vida) |

### Comandos
| Comando | Para qué |
|---------|----------|
| `aws sts get-caller-identity` | Con qué identidad estás trabajando (y el ID de cuenta) |
| `aws budgets create-budget` | Crear el presupuesto y sus alertas |
| `aws ec2 describe-regions` | Listar las regiones disponibles |
| `aws ec2 describe-availability-zones --region us-east-1` | Listar las zonas de una región |
| `aws iam create-group` / `attach-group-policy` | Crear un grupo y darle permisos |
| `aws iam create-user` / `create-login-profile` | Crear un usuario y su acceso a la consola |
| `aws iam add-user-to-group` | Meter al usuario en el grupo (así hereda los permisos) |
| `aws iam create-account-alias` | Alias para la URL de acceso |
| `aws ec2 run-instances --user-data file://user-data.sh` | Lanzar una instancia con script de arranque |
| `aws ec2 describe-instances --query ...PublicIpAddress` | Ver la IP pública actual |
| `aws ec2 create-volume --availability-zone --size` | Crear un volumen EBS en una zona |
| `aws ec2 attach-volume --volume-id --instance-id --device` | Adjuntarlo a la instancia |
| `aws efs put-lifecycle-configuration` | Mover a EFS-IA lo que no se usa |
