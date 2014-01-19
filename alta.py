# ­*­ coding: utf­8 ­*­
import os
import sys
import shutil
import MySQLdb
import getpass
user_name = sys.argv[1]

domain_name = sys.argv[2]

db_host = 'localhost'
usuario = 'root'
clave = 'usuario'
base_de_datos = 'USUARIOS'

db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave,
db=base_de_datos)

cursor = db.cursor()

mi_query = "SELECT username FROM usuarios WHERE username="+"'"+user_name+"'"


cursor.execute(mi_query)
usuarioexistente = cursor.fetchall()[0][0]

if usuarioexistente[0][0] == user_name:
        print "Ya existe el usuario no se dara de alta"
        exit()
else:
	print "El usuario no existe se procede a comprobar si existe el nombre de dominio"

if os.path.exists("/var/www/"+domain_name+""):
	print "El dominio ya esta en uso no se creara el usuario ni el dominio"
	exit()
else:
	print "El usuario y dominio introducidos son correctos, se procede a dar de alta..."

#Creamos usuarios
pass_user = getpass.getpass()

mi_insert = "INSERT INTO usuarios VALUES ("+"'"+user_name+"', md5("+"'"+pass_user+"'),'5001', '6001', '/srv/www/"+domain_name+"', '/bin/false', '1');"

cursor.execute(mi_insert)
db.commit()
db.close)

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
