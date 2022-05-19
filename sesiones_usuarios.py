import bcrypt
import sqlite3
from settings import BD
import uuid
from datetime import datetime

def conectar():
    cnx = sqlite3.connect(BD)
    return cnx

def guarda_usr(usuario, clave):
        
    #Encripta la clave
    salt = bcrypt.gensalt()
    byte_clave = clave.encode('utf-8')
    clave = bcrypt.hashpw(byte_clave, salt).decode()

    bd = conectar()
    cursor = bd.cursor()

    nuevo_id = cursor.execute(f"insert into usuario(nombre, clave) values ('{usuario}','{clave}');").lastrowid
    bd.commit()

    return carga_usuario(usuario)

def carga_usuario(usuario):
    bd = conectar()
    cursor = bd.cursor()
    cursor.execute(f'select clave from usuario where nombre ="{usuario}";')
    mi_usr = cursor.fetchone()
    if mi_usr:
        clave = mi_usr[0]
        return {'usuario':usuario, 'clave':clave}
    else:
        return None

def valida_usuario(clave, bd_clave):
    return bcrypt.checkpw(clave.encode('utf-8'), bd_clave.encode('utf-8'))


# Sesiones

def inicia_sesion(usuario):
    clave_sesion = str(uuid.uuid4())

    bd = conectar()
    cursor = bd.cursor()

    nuevo_id = cursor.execute(f"insert into sesiones(usuario, clave_sesion) values ('{usuario}','{clave_sesion}');").lastrowid
    bd.commit()
    if nuevo_id == None:
        return None
    else:
        return clave_sesion

def fin_sesion(clave_sesion):
    bd = conectar()
    cursor = bd.cursor()

    cursor.execute(f"delete from sesiones where clave_sesion = '{clave_sesion}'")
    bd.commit()

    return True    