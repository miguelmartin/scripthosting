# ­*­ coding: utf­8 ­*­
import os
import sys
import shutil
user_name = sys.argv[1]

domain_name = sys.argv[2]

#Añadimos al fichero /etc/bind/named.conf.local las zonas nuevas

linea1 = '\nzone ' +'"' +  domain_name +'"'  +'{\ntype master;\nfile "db.'+ domain_name +'"' +' ;\n}; '
linea2 = '\nzone "45.168.192.in-addr-arpa" {\ntype master;\nfile "db.45.168.192";\n};\n'
fichero = open("/etc/bind/named.conf.local","a")
fichero.write(linea1) 
fichero.write(linea2)
fichero.close 

#Creamos los ficheros de las zonas nuevas

plantillazona = open("plantillazona","r")
lineas = plantillazona.readlines() 
plantillazona.close
ficherozona = open("/var/cache/bind/db."+domain_name+"","w")
for linea in lineas:
	linea = linea.replace('domain_name',domain_name)
	ficherozona.write(linea)
ficherozona.close()
	
plantillainversa = open("plantillainversa","r")
lineas2 = plantillainversa.readlines()
plantillainversa.close
ficheroinversa = open("/var/cache/bind/db.45.168.192","w")
for linea2 in lineas2:
        linea2 = linea2.replace('domain_name',domain_name)
        ficheroinversa.write(linea2)
ficheroinversa.close()

os.system("service bind9 restart")

#Creamos el nuevo virtualhost y directorio web

shutil.copytree("html" , "/var/"+domain_name+"/")

plantillahost = open("plantillahost","r")
lineas3 = plantillahost.readlines()
plantillahost.close
ficherohost = open("/etc/apache2/sites-available/"+domain_name+"","w")
for linea3 in lineas3:
        linea3 = linea3.replace('domain_name',domain_name)
        ficherohost.write(linea3)
ficherohost.close()
os.system("a2ensite "+domain_name+"")
os.system("service apache2 restart")
