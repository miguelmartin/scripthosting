# ­*­ coding: utf­8 ­*­
import os
import sys
import shutil
import MySQLdb
import getpass
import string
from random import choice

#Recibimos como argumentos el nombre del usuario y el del dominio nuevo
user_name = sys.argv[1]
subdomain_name = sys.argv[2]

#Damos las credenciales para conectarnos a la base de datos
db_host = 'localhost'
usuario = 'root'
clave = 'usuario'
base_de_datos = 'proftpd'

#Realizamos la conexión y reamos el cursor
db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave,
db=base_de_datos)
cursor = db.cursor()

#Comprobamos si el nuevo usuario que queremos crear existe ya
mi_query = "SELECT userid FROM ftpuser WHERE userid="+"'"+user_name+"'"
cursor.execute(mi_query)
usuarioexistente = cursor.fetchall()

if usuarioexistente = () :
        print "No existe el usuario introducido"
        exit()
else:
	print "El usuario existe y se creara el subdominio"

mi_query2 = "select homedir from ftpuser where userid="+"'"+user_name+"'"
cursor.execute(mi_query2)
directorio_domain = cursor.fetchall()[0][0]
domain_name = directorio_domain[9:100]

#Añadimos al fichero /etc/bind/named.conf.local las zonas nuevas
linea1 = subdomain_name+'           CNAME           servidor'
ficherozona = open("/var/cache/bind/db."+domain_name+"","w")
fichero.write(linea1) 
fichero.close() 

	
#Creamos el virtualhost para phpmyadmin
plantillamysql = open("plantillasub","r")
lineas4 = plantillamysql.readlines()
plantillamysql.close()
ficheromysql = open("/etc/apache2/sites-available/"subdomain_name"."+domain_name+"","w")
for linea4 in lineas4:
        linea4 = linea4.replace('domain_name',domain_name)
	linea4 = linea4.replace('subdomain_name',subdomain_name)
	linea4 = linea4.replace('directorio_domain',directorio_domain)
        ficheromysql.write(linea4)
ficheromysql.close()
os.system("a2ensite "subdomain_name"."+domain_name+"> /dev/null")
os.system("service apache2 restart > /dev/null")
os.system("/etc/init.d/bind9 restart > /dev/null")
