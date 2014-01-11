# -*- coding: utf-8 -*-
from web import form
import re
import db

# Expresiones regulares necesarias:

formatoVisa=re.compile(r'[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}')


# Funciones necesarias para las validaciones

def esBisiesto(anio):
    if anio % 4 == 0 and anio % 100 != 0 or anio % 400 == 0:
        return True
    else:
        return False

def passCorrecto(username,passwd):
    print 'Comprobando password'
    datos==db.devuelveUsuario(username)
    if passwd==datos['password']:
        return True
    else:
        return False


# Formulario para iniciar sesión:

formularioLogin = form.Form(
            form.Textbox(
                "username",
                form.notnull, 
                class_="input-group input-group-sm", 
                id="loginUsernameId", 
                description="Nombre de usuario: "
            ),
            form.Password(
                "password",
                form.notnull,
                class_="input-group input-group-sm",
                id="loginPasswordId",
                description=u"Contraseña: "
            )
    )


# Formulario para insertar un nuevo usuario:

formularioInscripcion = form.Form(
            form.Textbox(
                "nombre",
                form.notnull, 
                class_="form-control", 
                id="nombreId",
                description="Nombre: " 
            ),
            form.Textbox(
                "apellidos",
                form.notnull, 
                class_="form-control", 
                id="apellidosId", 
                description="Apellidos: "
            ),
            form.Textbox(
                "dni",
                form.notnull,
                class_="form-control", 
                id="dniId", 
                description="DNI: "
            ),
            form.Textbox(
                "email",
                form.notnull,
                form.regexp(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}',
                 'Formato de email incorrecto'), 
                class_="form-control", 
                id="emailId", 
                description=u"Correo electrónico: "
            ),
            form.Dropdown(
                "dia", 
                [(d, d) for d in range(1,32)],
                id="diaID",
                description=u"Día de nacimiento: ",
            ),
            form.Dropdown(
                "mes",
                [(1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),
                (7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre')],
                id="mesID",
                description="Mes de nacimiento: "
            ),
            form.Dropdown(
                "anio", 
                [d for d in range(1930,2006)],
                id="anioID",
                description=u"Año de nacimiento: "
            ),
            form.Textarea(
                "direccion",
                form.notnull, 
                class_="form-control", 
                id="direccionId",
                description=u"Dirección: " 
            ),
            form.Textbox(
                "username",
                form.notnull, 
                class_="form-control", 
                id="usernameId", 
                description="Nombre de usuario: "
            ),
            form.Password(
                "password1",
                form.notnull,
                class_="form-control",
                id="password1Id",
                description=u"Contraseña: "
            ),
            form.Password(
                "password2",
                form.notnull,
                class_="form-control",
                id="password2Id",
                description=u"Repita la contraseña: "
            ),
            form.Radio(
                'formaPago',
                [["VISA","VISA  "],["contraReembolso","Contra reembolso"]],
                form.notnull,
                id="formaPagoId",
                description="Forma de pago: "
            ),
            form.Textbox(
                "visa",
                class_="form-control", 
                id="visaId", 
                description="Número de tarjeta VISA: ",
            ),
            form.Checkbox(
                "acepto",
                description="Acepto las condiciones de uso ",
                id="aceptoId",
                value="si"
            ),
            validators = [
                form.Validator(u"Fecha incorrecta", lambda x: ((int(x.mes)==2 and int(x.dia)<=28)) or 
                (int(x.mes) in [4,6,9,11] and int(x.dia)<31) or (int(x.mes) in [1,3,5,7,8,10,12]) 
                or (int(x.mes)==2 and int(x.dia)==29 and esBisiesto(x.anio))),
                form.Validator(u"La contraseña debe tener al menos 7 caracteres",lambda x: len(x.password1)>6),
                form.Validator(u"Las contraseñas no coinciden", lambda x: x.password1 == x.password2),
                form.Validator(u"Debe introducir un número de tarjeta válido",lambda x: (x.formaPago=="contraReembolso") 
                    or (x.formaPago=="VISA" and formatoVisa.match(x.visa))),
                form.Validator(u"Debe aceptar los términos y condiciones",lambda x: x.acepto=="si")
            ]
        ) 


# Formulario para mostrar los datos de un usuario y modificarlos:

formularioUserData = form.Form(
            form.Textbox(
                "nombre",
                form.notnull, 
                class_="form-control", 
                id="nombreId",
                description="Nombre: " 
            ),
            form.Textbox(
                "apellidos",
                form.notnull, 
                class_="form-control", 
                id="apellidosId", 
                description="Apellidos: "
            ),
            form.Textbox(
                "dni",
                form.notnull,
                class_="form-control", 
                id="dniId", 
                description="DNI: "
            ),
            form.Textbox(
                "email",
                form.notnull,
                form.regexp(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}',
                 'Formato de email incorrecto'), 
                class_="form-control", 
                id="emailId", 
                description=u"Correo electrónico: "
            ),
            form.Dropdown(
                "dia", 
                [(d, d) for d in range(1,32)],
                id="diaID",
                description=u"Día de nacimiento: ",
            ),
            form.Dropdown(
                "mes",
                [(1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),
                (7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre')],
                id="mesID",
                description="Mes de nacimiento: "
            ),
            form.Dropdown(
                "anio", 
                [d for d in range(1930,2006)],
                id="anioID",
                description=u"Año de nacimiento: "
            ),
            form.Textarea(
                "direccion",
                form.notnull, 
                class_="form-control", 
                id="direccionId",
                description=u"Dirección: " 
            ),
            form.Textbox(
                "username",
                class_="form-control", 
                id="usernameId", 
                description="Nombre de usuario: ",
                disabled='on'
            ),
            form.Password(
                "passwordAnterior",
                class_="form-control",
                id="passwordAngeriorId",
                description=u"Contraseña actual: "
            ),
            form.Password(
                "passwordNuevo",
                class_="form-control",
                id="passwordNuevoId",
                description=u"Introduzca la nueva contraseña: "
            ),
            form.Password(
                "passwordNuevo2",
                class_="form-control",
                id="passwordNuevo2Id",
                description=u"Repita la nueva contraseña: "
            ),
            form.Radio(
                'formaPago',
                [["VISA","VISA  "],["contraReembolso","Contra reembolso"]],
                form.notnull,
                id="formaPagoId",
                description="Forma de pago: "
            ),
            form.Textbox(
                "visa",
                class_="form-control", 
                id="visaId", 
                description="Número de tarjeta VISA: ",
            ),
            form.Checkbox(
                "acepto",
                description="Acepto las condiciones de uso ",
                id="aceptoId",
                value="si"
            ),
            validators = [
                form.Validator(u"Fecha incorrecta", lambda x: ((int(x.mes)==2 and int(x.dia)<=28)) or 
                (int(x.mes) in [4,6,9,11] and int(x.dia)<31) or (int(x.mes) in [1,3,5,7,8,10,12]) 
                or (int(x.mes)==2 and int(x.dia)==29 and esBisiesto(x.anio))),
                form.Validator(u"La contraseña actual es incorrecta", lambda x: (x.passwordAnterior=="") or (x.passwordAnterior!="" and passCorrecto(session.username,x.passwordAnterior)==True)),
                form.Validator(u"La contraseña debe tener al menos 7 caracteres",lambda x: (len(x.passwordNuevo)>6 or x.passwordNuevo=="")),
                form.Validator(u"Las contraseñas no coinciden", lambda x: x.passwordNuevo == x.passwordNuevo2),
                form.Validator(u"Debe introducir la contraseña actual", lambda x: (x.passwordAnterior=="" and x.passwordNuevo=="") or (x.passwordAnterior!="" and x.passwordNuevo!="")),
                form.Validator(u"Debe introducir un número de tarjeta válido",lambda x: (x.formaPago=="contraReembolso") 
                    or (x.formaPago=="VISA" and formatoVisa.match(x.visa))),
                form.Validator(u"Debe aceptar los términos y condiciones",lambda x: x.acepto=="si")
            ]
        ) 

formularioGrafica = form.Form(
            form.Textbox(
                "title",
                class_="input-group input-group-sm formElement", 
                id="titleInputId", 
                description=u"Título: "
            ),
            form.Textbox(
                "fila1",
                class_="input-group input-group-sm formElement", 
                id="fila1Id", 
                description=u"Fila 1: ",
                value="valor 1"
            ),
            form.Textbox(
                "n1",
                class_="input-group input-group-sm formElement", 
                id="n1Id", 
                description=u"Valor 1: ",
                value=5
            ),            
            form.Textbox(
                "fila2",
                class_="input-group input-group-sm formElement", 
                id="fila2Id", 
                description=u"Fila 2: ",
                value="valor 2"
            ),
            form.Textbox(
                "n2",
                class_="input-group input-group-sm formElement", 
                id="n2Id", 
                description=u"Valor 2: ",
                value=5
            ),
            form.Textbox(
                "fila3",
                class_="input-group input-group-sm formElement", 
                id="fila3Id", 
                description=u"Fila 3: ",
                value="valor 3"
            ),
            form.Textbox(
                "n3",
                class_="input-group input-group-sm formElement", 
                id="n3Id", 
                description=u"Valor 3: ",
                value=5
            ),
            form.Textbox(
                "fila4",
                class_="input-group input-group-sm formElement", 
                id="fila4Id", 
                description=u"Fila 4: ",
                value="valor 4"
            ),
            form.Textbox(
                "n4",
                class_="input-group input-group-sm formElement", 
                id="n4Id", 
                description=u"Valor 4: ",
                value=5
            ),
            form.Textbox(
                "fila5",
                class_="input-group input-group-sm formElement", 
                id="fila5Id", 
                description=u"Fila 5: ",
                value="valor 5"
            ),
            form.Textbox(
                "n5",
                class_="input-group input-group-sm formElement", 
                id="n5Id", 
                description=u"Valor 5: ",
                value=5
            ),    
    )