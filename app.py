from bottle import request,response,run,route,jinja2_view, TEMPLATE_PATH, redirect
from sesiones_usuarios import guarda_usr, valida_usuario, carga_usuario, inicia_sesion, fin_sesion
from settings import TEMPLATES

TEMPLATE_PATH.append(TEMPLATES)

@route('/')
@jinja2_view('index.html')
def index():
    info = {'title': 'Bienvenido.',
            'content': 'Esta es tu primera visita.'
    }


    #Visitas
    visits = request.get_cookie('visited')
    if visits:
        visits = int(visits) + 1
        info['content'] = f'Has estado aquí {visits} veces.'
    else:
        visits = 1
        info['content'] = f'Has estado aquí 1 vez.'



    response.set_cookie('visited', str(visits), samesite=None, secure=True)
    

    # Sesión de usuario
    clave_sesion = request.get_cookie('clave_sesion')
    if clave_sesion:
        info['clave_sesion'] = clave_sesion
    else:
        info['clave_sesion'] = ''

    return {'info':info}

@route('/login')
def login():
    
    nombre_usr = 'jose'
    clave_usr = 'secreta'
    
    mi_usr = carga_usuario(nombre_usr)
    if mi_usr:
        if valida_usuario(clave_usr,mi_usr['clave']):
            resp = inicia_sesion(nombre_usr)
            response.set_cookie('clave_sesion',resp)
    else:
        nuevo_usr = guarda_usr(nombre_usr,clave_usr)
        resp = inicia_sesion(nuevo_usr['usuario'])
        response.set_cookie('clave_sesion',resp)
    


    redirect('/')

@route('/logout')
def logout():
    fin_sesion(request.get_cookie('clave_sesion'))
    response.set_cookie('clave_sesion','')
    redirect('/')        


run(host='localhost', port=8000,debug=True,reloader=True)
