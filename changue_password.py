# ­*­ coding: utf­8 ­*­
import sys
import MySQLdb

#Variables que puede recibir el programa
opcion=(sys.argv[1])
user_name=(sys.argv[2])
passwdnew=(sys.argv[3])

if opcion == "-mysql":
        host = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="mysql")
        cursor=host.cursor()
        queryuser="select user from user where user='"+user_name+"';"
        cursor.execute(queryuser)
        resultado = cursor.fetchone()
	if resultado == None:
		print "Usuario incorrecto"
		exit()
        if resultado[0] == user_name:
                changuepasswd="SET PASSWORD FOR "+user_name+"@localhost = PASSWORD('"+passwdnew+"');"
                cursor.execute(changuepasswd)
                host.commit()
                print "Se ha actualizado la contraseña del usuario correctamente"
        else:
                print "El usuario introducido no existe"
               	exit()

elif opcion == "-ftp":
        host = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="proftpd")
        cursor=host.cursor()
        queryuser="select userid from ftpuser where userid='"+user_name+"';"
        cursor.execute(queryuser)
        resultado = cursor.fetchone()
        if resultado[0]== user_name:
                querypasswd="Update ftpuser set passwd = ENCRYPT('"+passwdnew+"')where userid='"+user_name+"';"
                cursor.execute(querypasswd)
                host.commit()
                print "Se ha actualizado la contraseña FTP"
        else:
                print "El usuario introducido no existe"
else:
        print "No selecciono ninguna accion"

