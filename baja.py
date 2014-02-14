# ­*­ coding: utf­8 ­*­
import os
import sys
import shutil
import MySQLdb
import getpass
import string
from random import choice
#Recibimos como argumentos el nombre del usuario y el del dominio nuevo
domain_name = sys.argv[1]

#Comprobamos que el domino que se quiere dar de baja existe
if os.path.exists("/srv/www/"+domain_name+""):
	print "El dominio existe y se procede a borrarlo"
else:
	print "El dominio que quiere dar de bajo no existe"
	exit()
#Damos las credenciales para conectarnos a la base de datos
db_host = 'localhost'
usuario = 'root'
clave = 'usuario'
base_de_datos = 'proftpd'

#Realizamos la conexión y reamos el cursor
db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave,
db=base_de_datos)
cursor = db.cursor()
#Borramos el usuario de mysql y el usuario ftp
print "Borrando usuario..."
select_user_name = "select userid from ftpuser where homedir like '%"+domain_name+"%';"
cursor.execute(select_user_name)
user_name = cursor.fetchall()[0][0]

mi_insert = "delete from ftpuser where homedir like '%"+domain_name+"%';"
cursor.execute(mi_insert)
borrar_usuario = "drop user my"+user_name+"@localhost ;"
cursor.execute(borrar_usuario)
db.commit()
db.close()
#Borrar ficheros DNS
os.remove("/var/cache/bind/db."+domain_name+"")
os.system("rm -r /srv/www/"+domain_name+"")
#Fichero named.conf.local
os.system("sed '/zone " + '"%s"'% domain_name + "/,/};/d' /etc/bind/named.conf.local > temporal")
os.system("mv temporal /etc/bind/named.conf.local")
#Borrar ficheros apache
os.remove ("/etc/apache2/sites-available/"+domain_name+"")
os.remove ("/etc/apache2/sites-available/mysql."+domain_name+"")
#Reiniciamos los servicios
os.system("a2dissite mysql."+domain_name+"> /dev/null")
os.system("a2dissite "+domain_name+"> /dev/null")
os.system("service apache2 restart > /dev/null")
os.system("/etc/init.d/bind9 restart > /dev/null")
