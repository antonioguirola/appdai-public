# -*- coding: utf-8 -*-

import re
import operator
import web
import config
import db
import forms
from view import *
from web.contrib.template import render_mako
from web import form
#Parser XML:
from lxml import etree
#Tweepy
import tweepy

# Para poder usar sesiones con web.py
web.config.debug = False

urls = (
	'/signup', 'formulario',
    '/login', 'login',
    '/logout', 'logout',
    '/user_data', 'user_data',
    '/rss', 'rss',
    '/charts', 'charts',
    '/maps', 'maps',
    '/twitter', 'twitter',
    '/twitterAuth','twitterAuth',
    '/', 'index'
)

app = web.application (urls, locals())

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':'',
    'username':'','contadorHistorial':0,'historial':[['',''],['',''],['','']]})

formularioLogin=forms.formularioLogin()

# TWITTER CONFIG
twitterSessionData = dict()
# Consumer keys and access tokens, used for OAuth
consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# utilizo los credenciales de mi cuenta
#access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
callback_url='http://localhost:8080/twitterAuth'


# MÉTODOS
def comprueba_identificacion (): 
    usuario = session.usuario   # Devuelve '' cuando no está identificado
    return usuario              # que es el usuario inicial 

def loadSession(args,section):
    #Comprobamos si hay una sesión abierta
        usuario = comprueba_identificacion ()
        if usuario:
            args['sesion']=usuario
            args['historial']=session.historial
            #añadimos la página al historial
            addToHistory(section)

def addToHistory(section):
    if section=='index':
        toAdd=['/','Inicio']
    elif section=='signup':
        toAdd=['/signup',u'Formulario de inscripción']
    elif section=='user_data':
        toAdd=['/user_data','Datos del perfil']
    elif section=='rss':
        toAdd=['/rss','Noticias RSS']
    elif section=='charts':
        toAdd=['/charts',u'Gráficas de Google']
    elif section=='maps':
        toAdd=['/maps',u'Mapa']
    elif section=='twitter':
        toAdd=['/twitter',u'Twitter']
    else:
        toAdd=['','']

    session.historial[session.contadorHistorial]=toAdd
    session.contadorHistorial=(session.contadorHistorial+1)%3

class index:
    def GET(self):

    	args={'title':'Pr&aacutectica 4 de DAI', 'texto':'Columna de la derecha',
        'formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'index')
            
    	return serve_template('index.html', **args)

class formulario:

    def GET(self):
    	
        f=forms.formularioInscripcion()

        args={'title':'Formulario de inscripci&oacute;n','form':f,'formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'signup')
        
    	return serve_template('formulario.html', **args)

    def POST(self):
        
        f=forms.formularioInscripcion()

        args={'title':u'Formulario de inscripción','form':f,'formularioLogin':formularioLogin}

        if f.validates(): 
            #si no existe el usuario se agrega a la base de datos
            datos=web.input()
            username=datos.username
            if db.devuelveUsuario(username)==None:
                args['passed']=True
                db.almacenaUsuario(datos)
            else:
                args['passed']=False
                args['msg']='El usuario ya existe'
            
        else:
            args['passed']=False

        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'signup')

        return serve_template('formulario.html',**args)

class user_data:

    def GET(self):
        
        f=forms.formularioUserData()

        args={'title':'Datos del usuario','form':f,'formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'user_data')

        #buscamos en la base de datos
        datos_usuario=db.devuelveUsuario(session.username)

        # Para debug se muestran los datos del usuario:
        #args['msg']=' | '.join(datos_usuario)

        # Relleno el formulario con los datos actuales:
        f.nombre.value=datos_usuario['nombre']
        f.apellidos.value=datos_usuario['apellidos']
        f.dni.value=datos_usuario['dni']
        f.email.value=datos_usuario['email']
        f.dia.value=int(datos_usuario['dia'])
        f.mes.value=int(datos_usuario['mes'])
        f.anio.value=int(datos_usuario['anio'])
        f.direccion.value=datos_usuario['direccion']
        f.username.value=session.username
        f.formaPago.value=datos_usuario['formaPago']
        #Si hay número de VISA lo indicamos:
        if 'visa' in datos_usuario.keys():
            f.visa.value=datos_usuario['visa']

        return serve_template('user_data.html', **args)

    def POST(self):
        
        f=forms.formularioUserData()

        args={'title':u'Datos del usuario','form':f,'formularioLogin':formularioLogin}

        if f.validates(): 
            args['passed']=True
            datos=web.input()
            db.modificaUsuario(session.username,datos)           
        else:
            args['passed']=False

        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'user_data')

        #buscamos en la base de datos
        datos_usuario=db.devuelveUsuario(session.username)

        # Para debug se muestran los datos del usuario:
        #args['msg']=' | '.join(datos_usuario)

        # Relleno el formulario con los datos actuales:
        f.nombre.value=datos_usuario['nombre']
        f.apellidos.value=datos_usuario['apellidos']
        f.dni.value=datos_usuario['dni']
        f.email.value=datos_usuario['email']
        f.dia.value=int(datos_usuario['dia'])
        f.mes.value=int(datos_usuario['mes'])
        f.anio.value=int(datos_usuario['anio'])
        f.direccion.value=datos_usuario['direccion']
        f.username.value=session.username
        f.formaPago.value=datos_usuario['formaPago']
        #Si hay número de VISA lo indicamos:
        if 'visa' in datos_usuario.keys():
            f.visa.value=datos_usuario['visa']

        return serve_template('user_data.html',**args)

class rss:
    def GET(self):

        args={'title':'RSS','formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'rss')

        #Actualización de los ficheros RSS que se van a utlizar:
        fileName='ultimas_noticias.xml'
        url='http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
        db.updateRSSFile(url,fileName)
        
        tree=etree.parse(fileName)
        items=tree.xpath('//channel/item')

        #print(items)

        newsDict=dict()
        for i in range(0,len(items)):
            newsDict[i]=dict()

            #Añadir el título
            tit=items[i].xpath('title/text()')
            if len(tit)>0:
                newsDict[i]['titulo']=tit[0]            

            #Añadir el autor
            creator = items[i].xpath('dc:creator/text()', namespaces=items[i].nsmap)
            if len(creator)>0:
                newsDict[i]['autor']=creator[0]            

            #Miniatura:
            thumbnail=items[i].xpath('enclosure/@url')
            if len(thumbnail)>1:
                newsDict[i]['imagen']=thumbnail[1]

            #Contenido:
            content=items[i].xpath('content:encoded/text()', namespaces=items[i].nsmap)
            if len(content)>0:
                newsDict[i]['contenido']=content[0]

            #Enlace:
            link=items[i].xpath('link/text()')
            if len(link)>0:
                newsDict[i]['enlace']=link[0]

        #print(newsDict)
        args['RSSFile']=newsDict            
        return serve_template('rss.html', **args)

class charts:
    def GET(self):

        args={'title':u'Gráficas de Google','formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'charts')
           
        args['formularioGrafica']=forms.formularioGrafica()

        return serve_template('charts.html', **args)

class maps:
    def GET(self):

        args={'title':u'Google Maps','formularioLogin':formularioLogin}
        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'maps')

        return serve_template('maps.html', **args)


class twitter:

    def GET(self):

        if 'api' in twitterSessionData.keys():
            api=twitterSessionData['api']
        else:            
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
            
            redirect_url= auth.get_authorization_url()
            twitterSessionData['request_token']= (auth.request_token.key,
                    auth.request_token.secret)
            
            return web.seeother(redirect_url)

        args={'title':u'Twitter','formularioLogin':formularioLogin}        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'twitter')

        #obtiene el timeline del usuario
        timeline=api.home_timeline()
        user_tweets=[]
        coordList=[]
        userCount=dict()

        #Creamos un diccionario con los tweets y su autor
        for i in range(0,len(timeline)):
            tweet=timeline[i]

            #print dir(tweet)
            #print tweet.coordinates
            #print dir(tweet.user)

            scrname='@'+tweet.user.screen_name
            user_tweets.insert(i, {
                'autor':tweet.author.name,
                'texto':unicode(tweet.text),
                'fecha':tweet.created_at,
                'coordenadas':tweet.coordinates,
                'screen_name':scrname
            })
            if tweet.coordinates!=None:
                c=[tweet.coordinates['coordinates'][0],tweet.coordinates['coordinates'][1]]
                coordList.append(c)

            #Aumentamos el contador de tweets del usuario
            if scrname in userCount.keys():
                userCount[scrname]+=1
            else:
                userCount[scrname]=1

        #Ordenamos de mayor a menor los usuarios en función del número de tweets suyos que aparecen:
        sorted_userCount = sorted(userCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        #print sorted_userCount

        args['tweetsSet']=user_tweets
        args['coordList']=coordList
        args['users']=sorted_userCount

        return serve_template('twitter.html', **args)

    def POST(self):

        args={'title':u'Twitter','formularioLogin':formularioLogin}        
        #cargar la sesión si la hay y añadir la página al historial:
        loadSession(args,'twitter')

        if 'api' in twitterSessionData.keys():
            api=twitterSessionData['api']
            print ' que pollas haces'
        else:            
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
            
            redirect_url= auth.get_authorization_url()
            twitterSessionData['request_token']= (auth.request_token.key,
                    auth.request_token.secret)
            
            return web.seeother(redirect_url)

        # Obtenemos el valor de búsqueda
        i = web.input()
        query  = i.queryField
        
        #realizamos la búsqueda
        timeline = api.search(q=query, count=100)
        
        queryResults=[]
        coordList=[]
        userCount=dict()

        #Creamos un diccionario con los tweets, autor, fecha y coordenadas.
        for i in range(0,len(timeline)):
            tweet=timeline[i]

            scrname='@'+tweet.user.screen_name
            queryResults.insert(i, {
                'autor':tweet.author.name,
                'texto':unicode(tweet.text),
                'fecha':tweet.created_at,
                'coordenadas':tweet.coordinates,
                'screen_name':scrname
            })
            if tweet.coordinates!=None:
                c=[tweet.coordinates['coordinates'][0],tweet.coordinates['coordinates'][1]]
                coordList.append(c)

            #Aumentamos el contador de tweets del usuario
            if scrname in userCount.keys():
                userCount[scrname]+=1
            else:
                userCount[scrname]=1

        #Ordenamos de mayor a menor los usuarios en función del número de tweets suyos que aparecen:
        sorted_userCount = sorted(userCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        #print sorted_userCount

        args['tweetsSet']=queryResults
        args['coordList']=coordList
        args['users']=sorted_userCount

        return serve_template('twitter.html', **args)

class login:
    def POST(self):
        #comprobamos los datos introducidos por el usuario
        i = web.input()
        usuario  = i.username
        password = i.password
        
        #buscamos en la base de datos
        datos_usuario=db.devuelveUsuario(usuario)
        if datos_usuario!=None:
            #Comprobamos la contraseña, que está en la posición 8
            if password==datos_usuario['password']:
                session.usuario = datos_usuario['nombre'] #Nombre del usuario
                session.username = datos_usuario['username'] #Username
            return web.seeother('/')
        else:
            args={'title':'Pr&aacutectica 4 de DAI', 'texto':'Columna de la derecha',
        'formularioLogin':formularioLogin,'msg':u'Usuario y/o contraseña incorrectos'}
            return serve_template('index.html', **args)
        
class logout:
    def GET(self):
        session.kill()
        return web.seeother('/')

class twitterAuth:
    def GET(self):
        i=web.input()
        verifier=i.oauth_verifier

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        token = twitterSessionData['request_token']
     
        auth.set_request_token(token[0], token[1])
     
        try:
                auth.get_access_token(verifier)
        except tweepy.TweepError:
                print 'Error! Failed to get access token.'
     
        #now you have access!
        api = tweepy.API(auth)

        twitterSessionData['api']=api
        twitterSessionData['access_token_key']=auth.access_token.key
        twitterSessionData['access_token_secret']=auth.access_token.secret

        return web.seeother('/twitter')
      
if __name__ == "__main__":
    app.run()
    