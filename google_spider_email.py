# -*- coding: utf-8 -*-
## by kase: kase@boredsoft.com  
import requests,re,os,time,sys
from argparse import ArgumentParser, RawTextHelpFormatter


parser = ArgumentParser(description="google dorks email spider ", version="1.0", formatter_class=RawTextHelpFormatter) 
## -url
parser.add_argument("-b",  dest="busqueda", help='Cadena a buscar en google entre comillas')
## -max_links links 
parser.add_argument("-p",  dest="paginas", help='Maximo de paginas a analizar en google (cada pagina contiene 10 enlaces) por defecto 10')
argumento = parser.parse_args()

dominio = 'http://google.com.mx'
mailsrch = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|mx|com\.mx|xxx|tv|tk)\b")
urlssrch = re.compile(r'href=[\'"]?([^\'" >]+)') 
googlesrch = re.compile(r'href=[\'"]?/url\?q=([^\'" &]+)')
contador = 0
links_internos = []
links_visitados = []
emails_capturados = []
if not argumento.paginas: 
	paginas = 10
else:
	paginas = argumento.paginas

## recorre las paginas de google (de 10 en 10)
for x in range(0,paginas):
	r=requests.get(dominio+''+'/search?q=%s&start=%s&num=100' % (argumento.busqueda,contador))
	contador +=100	

	links_google = googlesrch.findall( r.text)
	##recorre los links que arroje los resultados de google	
	for link in links_google:
		time.sleep(15)		
		r2=requests.get(link)
		emails = mailsrch.findall(r2.text)
		##detecta los emails encontrados en la web de resultado		
		for email in  emails:
			if email not in emails_capturados:
				emails_capturados.append(email)		
		## recorre un nivel en los enlaces de la web resultado bajo la teoria de que deben ser de tematica similar		
		links = urlssrch.findall( r2.text)
	
		########## informe de pantalla	
		if sys.platform.startswith('win'):
		    # Windows
		    os.system('cls')
		elif sys.platform.startswith('linux'):
		    # Linux
		    os.system('clear')
		elif sys.platform.startswith('cygwin'):
		    # Windows (Cygwin)
		    os.system('cmd /c cls')
		elif sys.platform.startswith('darwin'):
		    # MacOSX
		    os.system('clear')
		elif sys.platform.startswith('freebsd'):
		    # FreeBSD
		    os.system('clear')	
		print 'parametro de busqueda: ' , argumento.busqueda 
		print 'pagina checada: ', contador/10
		print 'paginas por checar: ', paginas - (contador/10)
		print 'emails capturados: ', len(emails_capturados)
		print 'url victima actual: ', r2.url	
		##fin de informe de pantalla
		
		while links:
			try:			
				link = links.pop()						
				if not link[0] == '/':				
					r3=requests.get(link)
				##else:  falta codigo para detectar el dominio :(
			except:
				ci = os.system('ping -c 1 google.com') ## checa si hay conexion de internet
				if ci == 0:  #si existe conexion elimina el enlace muerto 
					link = links.pop()
			
			#guarda emails de el nivel 2.
			emails = mailsrch.findall(r3.text)
			for email in  emails:
				if email not in emails_capturados:
					emails_capturados.append(email)

f = open('google_%s.txt' % argumento_busqueda.replace('.','_'),'w+')
f.write("\n".join(emails_capturados))
f.close()

