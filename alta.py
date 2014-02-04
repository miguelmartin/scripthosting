# ­*­ coding: utf­8 ­*­
import os
import sys
import shutil
import MySQLdb
import getpass

#Recibimos como argumentos el nombre del usuario y el del dominio nuevo
user_name = sys.argv[1]
domain_name = sys.argv[2]

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

if usuarioexistente != () :
        print "Ya existe el usuario no se dara de alta"
        exit()
else:
	print "El usuario no existe se procede a comprobar si existe el nombre de dominio"

#Ahora una vez que se a comprobado que el usuario no existe se comprueba la existencia del dominio
if os.path.exists("/srv/www/"+domain_name+""):
	print "El dominio ya esta en uso no se creara el usuario ni el dominio"
	exit()
else:
	print "El usuario y dominio introducidos son correctos, se procede a dar de alta..."
	print domain_name
#Pedimos contraseña del nuevo usuario
pass_user = getpass.getpass()
print "Tu contraseña nueva es: "+pass_user
#Consultamos el ultimo uid para ponerle los nuevos al usuario
my_query2 = "select uid from ftpuser order by uid desc limit 1;"
cursor.execute(my_query2)
uids = cursor.fetchall()
uidnuevo = uids[0][0]+1
uidnuevo = str(uidnuevo)
#Creamos el nuevo usuario en la base de datos
print "Creando nuevo usuario..."
mi_insert = "INSERT INTO `ftpuser` VALUES ('', "+"'"+user_name+"', ENCRYPT("+"'"+pass_user+"'), "+"'"+uidnuevo+"', 2001, '/srv/www/"+domain_name+"', '/sbin/nologin', 0, '', '');"
cursor.execute(mi_insert)
crear_usuario = "GRANT ALL ON "+user_name+".* TO "+user_name+"@localhost IDENTIFIED BY "+"'"+pass_user+"';"
cursor.execute(crear_usuario)
db.commit()
db.close()

#Añadimos al fichero /etc/bind/named.conf.local las zonas nuevas
linea1 = '\nzone ' +'"' +  domain_name +'"'  +'{\ntype master;\nfile "db.'+ domain_name +'"' +' ;\n}; '
linea2 = '\nzone ' +'"' +  domain_name +''  +'.in-addr-arpa" {\ntype master;\nfile ' +'"' +  domain_name +'.inver"'  +';\n};\n'
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
ficheroinversa = open("/var/cache/bind/db."+domain_name+".inver","w")
for linea2 in lineas2:
        linea2 = linea2.replace('domain_name',domain_name)
        ficheroinversa.write(linea2)
ficheroinversa.close()

os.system("service bind9 restart")

#Creamos el nuevo virtualhost y directorio web
shutil.copytree("html" , "/srv/www/"+domain_name+"/")

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
