#coding: utf-8

import sys
import MySQLdb
import os
from random import choice
import string


#pedimos el nombre y el dominio que se usara

nombre = (sys.argv[1])
dominio = (sys.argv[2])


#siguiente paso: conectarnos a la bbdd

conexion = MySQLdb.connect(host = "localhost", user = "root", passwd = "usuario", db = "hosting")
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="hosting", # your username
                      passwd="hosting", # your password
                      db="hosting") # name of the data base
cursor = conexion.cursor()






Script modelo:

import MySQLdb

db = MySQLdb.connect(host="192.168.100.1", # your host, usually localhost
                     user="conexion", # your username
                      passwd="conexion", # your password
                      db="conexion") # name of the data base

cur = db.cursor()

sql = 'select * from maillot'

cur.execute(sql)

resultado=cur.fetchall()

for registro in resultado:
        print "Codigo: ",registro[0],"Tipo: ",registro[1],"Color: ",registro[2],"Premio: ",registro[3]