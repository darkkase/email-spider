email-spider
============

spyder email web..  recolect some email from web :3

* acepta parametros 
-url       obligatorio con formato  http://somthing.com/   (la / final es necesaria)
-max_links  maxima cantidad de links a analizar antes de cortar el programa y guardar
-max_emails  maxima cantidad de emails a obtener antes de finalizar el programa y guardar
-external    acepta links externos, pero si no se usa junto con max_links o max_emails el programa nunca se detendra :(

** si la conexion de internet se cae el programa espera 30 segundos para reanudarse
** no se traba con enlaces muertos
** uso de "sort" para revisar enlaces con mayor probabilidad de tener email despues de cierto tiempo 

Citar
fix 3.0
soporte para mas sistemas operativos
mejor detección de emails mediante el regex
fix v 2.0
ahora detecta mas tipos de urls internas
ahora detecta si es windows o linux para usar el comando correcto de limpiar pantalla.


http://foro.elhacker.net/scripting/script_para_sacar_emails_de_paginas_webs_python_v30-t389036.0.html
