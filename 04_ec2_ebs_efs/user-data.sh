#!/bin/bash
# Curso AWS · Vídeo "Curso Completo de AWS (Amazon Web Services) | Desde CERO en ESPAÑOL!" de Joan Amengual
# Tramo "EC2 demo" 1:13:27: https://www.youtube.com/watch?v=NxhLT4ehhOw&t=4407s
# Apunte: apuntes/04-ec2-ebs-efs.md
#
# Script de datos de usuario (user data) de la demo: instala Apache y publica una página
# que dice desde qué instancia responde. Se ejecuta como root y SOLO en el primer arranque.
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hola mundo desde $(hostname -f)</h1>" > /var/www/html/index.html
