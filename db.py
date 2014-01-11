# -*- coding: utf-8 -*-

import config
import pymongo
from pymongo import MongoClient
from datetime import *
from urllib2 import *
import urllib
import time

# Método para conectar a la base de datos
def conectar(collection):
	# Connection to Mongo DB
	try:
		# Servidor MongoDB local:
	    #conn=pymongo.MongoClient()
	    # Servidor MongoDB en MongoLab:
	    conn = MongoClient("dsxxxxx.mongolab.com", <puerto>)
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	
	# Busca una base de datos y si no, la crea
	db=conn['appdai']
	# Servidor MongoDB en Mongolab:
	db.authenticate("user", "password")

	# Busca una colección y si no, la crea
	if collection=='users':
		col = db.users
	elif collection=='rssFile':
		col = db.rssFile

	return col


# Almacena un usuario en la base de datos
def almacenaUsuario(datos):
	colUsuarios=conectar('users')

	dto={
		'nombre':datos.nombre,
		'apellidos':datos.apellidos,
		'dni':datos.dni,
		'email':datos.email,
		'dia':datos.dia,
		'mes':datos.mes,
		'anio':datos.anio,
		'direccion':datos.direccion,
		'username':datos.username,
		'password':datos.password1,
		'formaPago':datos.formaPago
		}
	
	if datos.formaPago=="VISA":
		dto['visa']=datos.visa

	colUsuarios.insert(dto)

# Devuelve una lista si el username se encuentra en la BS o None en caso contrario
def devuelveUsuario(username):
	colUsuarios=conectar('users')

	return colUsuarios.find_one({'username':username})


# Modifica los datos de un usuario
def modificaUsuario(username,datos):
	colUsuarios=conectar('users')

	# vemos si se ha modificado la contraseña
	if datos.passwordNuevo!='':
		passwd=datos.passwordNuevo
	else:
		#mantenemos la contraseña antigua
		user=devuelveUsuario(username)
		passwd=user['password']

	dto={
		'nombre':datos.nombre,
		'apellidos':datos.apellidos,
		'dni':datos.dni,
		'email':datos.email,
		'dia':datos.dia,
		'mes':datos.mes,
		'anio':datos.anio,
		'direccion':datos.direccion,
		'username':username,
		'password':passwd,
		'formaPago':datos.formaPago
		}
	
	if datos.formaPago=="VISA":
		dto['visa']=datos.visa

	colUsuarios.update({'username':username},dto)


# Descarga un fichero RSS o lo actualiza si han pasado más de 10 minutos
# desde la última actualización
def updateRSSFile(url,fileName):
	# Buscamos el fichero en la BD:
	col=conectar('rssFile')
	file=col.find_one({'fileName':fileName})
	print file

	dto={
		'date':int(time.time()),
		'fileName':fileName
		}

	if file==None:
		print 'Descargando por primera vez RSS'
		#Descaramos el archivo:
		a,b=urllib.urlretrieve(url,r'./'+fileName)
		# Guardamos la info en la BD:
		col.insert(dto)
	else:
		previousDate=file['date']
		actualDate=int(time.time())
		#Comprobamos que la diferencia sea mayor que 10 min para actualizar:
		elapsedTime=int((actualDate-previousDate)/60)
		if elapsedTime>10:
			print 'Actualizando archivo RSS'
			#Descaramos el archivo:
			a,b=urllib.urlretrieve(url,r'./'+fileName)
			#Actualizamos la info en la BD:
			col.update({'fileName':fileName},dto)
		else:
			print 'No es necesario actualizar'

