# -*- coding: utf-8 -*-
## by kase: kase@boredsoft.com   colaboraciones: EleKtro H@cker
import requests,re,os,time,sys
from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(description="email spider", version="3.0", formatter_class=RawTextHelpFormatter) 
## -url
parser.add_argument("-url",  dest="url", help='url a analizar en formato http://web.com/')
## -max_links links 
parser.add_argument("-max_links",  dest="max_links", help='maximo de links internos a analizar')
## -max_emails emails
parser.add_argument("-max_emails",  dest="max_emails", help='maximo de emails a analizar')
## -external  default False
parser.add_argument("-external",  dest="external", help='investigar links externos [si|no]')

argumento = parser.parse_args()



url_web = argumento.url
url_web_limpio = argumento.url.replace('http://','').replace('/','').replace('www.','')
links_internos = ['/']
links_visitados = []
emails_capturados = []
mailsrch = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum|mx|com\.mx|xxx|tv|tk)\b")
#old mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{2,6}')
urlssrch = re.compile(r'href=[\'"]?([^\'" >]+)') 
contador = 0
while links_internos:
	try:	
		## saca el ultimo link de la lista	
		##print links_internos		
		link = links_internos.pop()
		## añade ese link a visitados, para no volverlo a tener en cuenta
		links_visitados.append(link)
		if link[0] == '/' or link == '':		
			r=requests.get(url_web+''+link)
		else:
			r=requests.get(link)		
		links = urlssrch.findall( r.text)
		##print 'xxxxxxxxxxxxx', links		
		emails = mailsrch.findall(r.text)	
		## guarda todos los emails que se topa checando que no existan repeticiones
		for email in  emails:
			if email not in emails_capturados:
				emails_capturados.append(email)	
		## guarda todos los links internos que se tope checando que no existan en la cola o en vistados	
		for link in links:
			if not argumento.external:  ## verifica si usar enlaces externos o no
				if link[0] == '/' or url_web_limpio in link:
					if link not in links_internos and link not in links_visitados:
						links_internos.append(link)
			elif  argumento.external == 'si':
				if link not in links_internos and link not in links_visitados:
					links_internos.append(link)
		contador +=1	
		## informacion en pantalla
		if contador % 50 == 0:
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
			print 'web atacada:', url_web
			print 'total de emails obtenidos:', len(emails_capturados)	
			print 'urls recorridas: ', len(links_visitados)
			print 'urls faltantes: ', len(links_internos)		
			print '-----  (~._.)~ '
		## pequeño arreglo para tener mas chanse de optener emails en web grandes
		## primero analiza los enlaces internos mas cortos  y despues de un tiempo, analiza los mas largos primero
		## en paginas tipo blog, los enlaces mas largos son los de las post con comentarios donde posiblemente existan emails		
		if contador %10000 == 0:	 
			if contador <= 10000:
				 links_internos.sort(reverse=True)
			else:
				links_internos.sort()
		## si ahi un maximo de links internos  rompe el ciclo y termina
		if argumento.max_links:
			if contador >= int(argumento.max_links):	
				break
		## si ahi un maximo de emails capturados rompe el ciclo y termina
		if argumento.max_emails:
			if len(emails_capturados) >= int(argumento.max_emails):
				break
	## si la conexion se cae duerme el proceso 20 segundos y reintenta
	except:
		r = os.system('ping -c 1 google.com') ## checa si hay conexion de internet
		if r == 0:  #si existe conexion elimina el enlace muerto 
			link = links_internos.pop()
		else: ##sino espera 20 segundos a que se reanude la conexion de internet
			time.sleep(30)
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
			print 'web atacada:', url_web
			print 'total de emails obtenidos:', len(emails_capturados)	
			print 'urls recorridas: ', len(links_visitados)
			print 'urls faltantes: ', len(links_internos)		
			print '-----  (~._.)~ CONEXION CAIDA, ESPERANDO 30 SEGUNDOS (X__X)'

f = open('%s.txt' % url_web.replace('http://','').replace('/','').replace('.','_'),'w+')
f.write("\n".join(emails_capturados))
f.close()
