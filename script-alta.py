#coding: utf-8

import sys
import MySQLdb
import os
from random import choice
import string


#pedimos nombre y dominio

nombre = (sys.argv[1])
dominio = (sys.argv[2])


#siguiente paso: conectarnos a la bbdd

conexion = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="hosting", # your username
                      passwd="hosting", # your password
                      db="hosting") # name of the data base

cursor = conexion.cursor()

consulta_usuario = 'select username from usuarios where username = '%s';' %nombre

cursor.execute(consulta_usuario)

consulta_usuario=cursor.fetchone()

if consulta_usuario != None:
	print "Ese usuario ya está registrado"
	sys.exit
else:
	consulta_dominio = "select dominio from usuarios where dominio = '%s';" %dominio
	cursor.execute(consulta_dominio)
	consulta_dominio=cursor.fetchone()

	if consulta_dominio != None:
		print "Ese dominio ya existe"
		sys.exit
	else:
		os.system("mkdir /srv/www/%s" %nombre)
		os.system("cp /var/www/index.html /srv/www/%s" %nombre)
        fichero = "/home/ale/templates/vhost"
        r_host = open(fichero,"r")
        w_host = open('/etc/apache2/sites-available'+dominio,"w")
        buffer_fichero = r.host.read()
        read_buffer_1 = buffer_fichero.replace("**usuario**", nombre)
        read_buffer_2 = read_buffer_1.replace("**dominio**", dominio)
        w_host.write(read_buffer_2)
        r_host.close()
        w_host.close()
        os.system("a2ensite "+dominio)
        os.system("service apache2 restart")



        #generamos una contrasenya aleatoria
        def GenPasswd(n):
            return ''.join([choice(string.letters + string.digits) for i in range(n)])
            contrasenna=GenPasswd(8)
            print"esta es tu contrasenna para el usuario %s ftp:"%nombre, contrasenna

			#insertamos el usuario en mysql
            consultauid="select max(uid) from usuarios;"
            cursor.execute(consultauid)
            consulta_uid = cursor.fetchone()
            #si la tabla está vacía introduce el 5001
            if consulta_uid[0] == None:
                conuid = "5001"
            else:
                conuid = str(int(consulta_uid[0])+1)
            usermysql="insert into usuarios values('"+ nombre+"'," +"PASSWORD('"+contrasenna+"'),"+conuid+",33,'/srv/www/"+nombre+"',"+"'/bin/false',"+"1,'"+dominio+"');"
            cursor.execute(usermysql)
            conexion.commit()
            #cambiamos los permisos del directorio para que el usuario pueda subir datos y acceder apache
            chown="chown "+conuid+":www-data /srv/www/"+nombre+" -R"
            chmod="chmod 770 -R /srv/www/"+nombre
            os.system(chown)
            os.system(chmod)


            #creamos una base de datos con una contraseña para el usuario
            cursor.execute("create database my"+nombre+";")
            passwdMysql=GenPasswd(8)
            #print "pass mysql "+passwdMysql
            grantPerm="grant all on my"+nombre+".* to 'my"+nombre+"'@'localhost' identified by '"+passwdMysql+"';"
            print "la contraseña del musuario my"+nombre+" es: " + passwdMysql
            cursor.execute(grantPerm)
            conexion.commit()


            #creamos la zona dns para el usuario que se esta creando
            ficherodominio="/home/ale/templates/db.plantilla"
            domain=open(ficherodominio, "r")
            filew = open('/var/cache/bind/db.'+dominio, "w")
            buff = domain.read()
            variable1='**dominio**'
            rbuff = buff.replace(variable1, dominio)
            filew.write(rbuff)
            domain.close()
            filew.close()


            #creamos la nueva zona
			fichzona="/home/ale/templates/zona"
            zonadom=open(fichzona,"r")
            zonabuff = zonadom.read()
            char1='**dominio**'
            cambio = zonabuff.replace(char1, dominio)
            g=open("/etc/bind/named.conf.local","a")
            g.write(cambio)
            g.close()
            zonadom.close()


            #reiniciamos el servidor dns
            rebootdns = os.system("service bind9 restart")
            print "El usuario se ha creado correctamente"