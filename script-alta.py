#coding: utf-8

import sys
import MySQLdb
import os
from random import choice
import string


#pedimos nombre y dominio

usuario = (sys.argv[1])
dominio = (sys.argv[2])


#siguiente paso: conectarnos a la bbdd

conexion = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="hosting", # your username
                      passwd="hosting", # your password
                      db="hosting") # name of the data base

cursor = conexion.cursor()

consulta_usuario = 'select username from usuarios where username = '%s';' %usuario

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






if os.path.isdir("/var/www/%s" % usuario) = False
and os.path.isfile("/etc/apache2/sites-available/%s" %dominio) = False:
	os.system("mkdir /var/www/%s" %usuario)
else:
	print "El usuario o el dominio ya existen, introduzca otro usuario y dominio por favor." % (usuario)
	exit()



