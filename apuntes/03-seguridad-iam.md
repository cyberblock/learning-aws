# 03 · Seguridad e IAM

Vídeo original: [Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s) · Autor: [Joan Amengual](https://www.youtube.com/channel/UCQB8dgeFkuKXVtzweRM_Zfw) · Duración: 14:04

**Tramo del vídeo:** 0:53:05 – 1:07:09

| Capítulo | Inicio |
|----------|--------|
| Seguridad IAM | [0:53:05](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3185s) |
| Qué es IAM | [0:53:36](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3216s) |
| Primer usuario IAM | [0:57:44](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3464s) |
| Uso usuario IAM | [1:02:54](https://www.youtube.com/watch?v=NxhLT4ehhOw&t=3774s) |

**Código:** [`03_iam/`](../03_iam/): política JSON de ejemplo y comandos de la CLI equivalentes.

## Resumen

IAM (*Identity and Access Management*) decide **quién puede hacer qué** en la cuenta. Es un servicio
**global**: no se elige región. La cuenta que se crea al registrarse es la **root**, y no se usa para
trabajar: se crea un **usuario IAM**, se mete en un **grupo** y el grupo lleva las **políticas** (documentos
JSON) con los permisos. La regla que gobierna todo es el **mínimo privilegio**: solo los permisos que
hacen falta, ni uno más.

## Usuarios, grupos y políticas

- **Usuario:** una identidad para una persona (o para un sistema). Puede tener contraseña para la consola
  y/o claves de acceso para la CLI.
- **Grupo:** una bolsa de usuarios que comparten permisos. Se agrupan por el papel de cada uno:
  desarrollo, operaciones, auditoría...
- Reglas de los grupos:
  - Un grupo contiene **usuarios**, nunca otros grupos: **no hay subgrupos**.
  - Un usuario puede estar en **varios grupos** a la vez (alguien de operaciones que además audita).
  - Estar en un grupo es **opcional**: se pueden adjuntar políticas directamente al usuario.
- **Política:** documento JSON con los permisos. Se adjunta a un grupo (lo habitual) o a un usuario.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ec2:Describe*", "elasticloadbalancing:Describe*"],
      "Resource": "*"
    }
  ]
}
```

| Campo | Qué significa |
|-------|----------------|
| `Version` | Versión del lenguaje de políticas. Siempre `2012-10-17` |
| `Effect` | `Allow` o `Deny` |
| `Action` | Operaciones de la API: `servicio:Operación`. Admite comodín (`ec2:Describe*`) |
| `Resource` | Sobre qué recursos se aplica. `"*"` = todos |
| `Sid` | Etiqueta opcional para identificar la sentencia |

Esto **no es programación**: es un documento de datos. Lo que se declara son llamadas a la API, las mismas
que hace la consola por debajo.

> **Nota de precisión.** `2012-10-17` no es la fecha en la que se escribe la política: es la versión del
> lenguaje. Se pone tal cual siempre.

> **Nota de precisión.** Por defecto **todo está denegado**. Un permiso solo existe si alguna política lo
> permite de forma explícita, y un `Deny` explícito **gana siempre** sobre cualquier `Allow`.

## Crear el primer usuario IAM

En la consola, servicio **IAM** → *Usuarios* → *Crear usuario*:

1. **Nombre** del usuario.
2. **Acceso a la consola:** el asistente ofrece dos caminos — *Identity Center* (el recomendado para
   organizaciones, se ve más adelante) o un **usuario IAM** normal, que es el del vídeo.
3. **Contraseña** generada automáticamente o personalizada, marcando *requerir cambio de contraseña en el
   primer inicio de sesión*.
4. **Permisos:** agregar a un grupo, copiar los de otro usuario o adjuntar políticas directamente.
   En el vídeo se crea el grupo `admin` con la política gestionada **`AdministratorAccess`**.
5. Al terminar, la consola muestra usuario y contraseña una sola vez y permite enviar las instrucciones
   de acceso por correo.

Con la CLI, lo mismo está en [`03_iam/cli-usuario-iam.sh`](../03_iam/cli-usuario-iam.sh):

```bash
aws iam create-group --group-name admin
aws iam attach-group-policy --group-name admin \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam create-user --user-name joan
aws iam create-login-profile --user-name joan --password '...' --password-reset-required
aws iam add-user-to-group --user-name joan --group-name admin
```

> **Nota de precisión.** `AdministratorAccess` da permiso sobre **todo**, así que ese usuario es casi tan
> peligroso como el root. Sirve para aprender, pero choca con el mínimo privilegio del que habla el propio
> vídeo. En una cuenta real: políticas de solo lectura para el día a día y permisos amplios únicamente
> cuando toca. Un ejemplo está en [`politica-solo-lectura.json`](../03_iam/politica-solo-lectura.json).

> **Nota de precisión.** El vídeo no lo menciona: activa **MFA** en el usuario root y en cualquier usuario
> con permisos amplios. Es la protección que más rendimiento da por el tiempo que cuesta.

## Alias de cuenta y acceso

- El ID de cuenta son **12 dígitos**, incómodos de recordar. En el panel de IAM se puede crear un **alias**
  (`joan-aws`), y la URL de acceso pasa a ser legible:

```
https://<alias>.signin.aws.amazon.com/console
https://<id-de-12-digitos>.signin.aws.amazon.com/console   # sigue funcionando
```

- La pantalla de inicio de sesión distingue **usuario root** (correo + contraseña) de **usuario IAM**
  (alias o ID de cuenta + nombre de usuario + contraseña).
- Una vez dentro, arriba a la derecha aparece `usuario @ alias`: así se sabe con qué identidad se trabaja.
- Truco del vídeo: abre la sesión del usuario IAM en **otro navegador o ventana privada** para no perder la
  sesión de root.

### Comprobar con qué identidad estás

```bash
aws sts get-caller-identity
```

```json
{
  "UserId": "AIDA...",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/joan"
}
```

> **Nota de precisión.** El alias de cuenta es **único en todo AWS** y solo puede haber **uno por cuenta**:
> si el que quieres está cogido, el comando falla. Crear otro sustituye al anterior.

## Errores típicos

- Trabajar a diario con el usuario **root** (o compartirlo). El root solo para lo que nadie más puede hacer:
  cerrar la cuenta, cambiar el plan de soporte, datos de facturación.
- Dar `AdministratorAccess` "para que no moleste" y dejarlo puesto.
- Adjuntar políticas usuario a usuario en lugar de al grupo: acaba siendo imposible saber quién puede qué.
- Buscar IAM en una región concreta. Es **global**; el selector de región ni siquiera aplica.

## Ejercicios

En [`03_iam/ejercicios`](../03_iam/ejercicios/):

1. Construye el documento JSON de una política que permita unas acciones dadas.
2. Calcula la URL de inicio de sesión a partir del alias (o del ID de cuenta).
3. Decide si una política permite una acción, teniendo en cuenta los comodines (`ec2:Describe*`).
4. **Arregla este código:** una función que detecta políticas de administrador y confunde `Action` con
   `Resource`, ignora los `Deny` y no soporta listas.
