import zmq
import os
import socket as sk
from shutil import rmtree

def getIp():
    
    # Obtengo la ip actual de la maquina donde se ejecuta el servidor (si no hay conexion a red devuelve la dir localhost 127.0.0.1)
    nombre = sk.gethostname()
    direccion = sk.gethostbyname(nombre)
    return direccion

#La estructua de carpetas en el servidor debe ser Artista -> Album -> Cancion

# Variables Globales -------------------------------------------------
ctx = zmq.Context() # Contexto para creacion de sockets
PATH = None   # Ruta donde se encuentran los archivos del servidor
MY_FILES = {} # Diccionario con la estructura de carpetas y archivos del servidor
IP_PROXY = "localhost:6000"
PORT = "5555"
SERVER_DIR = getIp()+":"+PORT #Direccion en la que esta el servidor actual( se debe cambiar el puerto para cada servidor ejecutado en la misma maquina)

# ------------------------------------------------------

def make_server_dir():

    # Se crea la carpeta del servidor inicialmente vacia, a la cual se cargaran los archivos a compartir
    # Si ya existe la carpeta no se hace nada
    global PATH
    directorio = os.getcwd()
    carpeta = "/servidor"+IP_SERVER
    ruta = directorio+carpeta
    try:
        # Verificar si ya existe la carpeta en la ruta (anteriores ejecuciones) 
        os.stat(ruta)
    except:
        # Crea la carpeta para el funcionamiento del servidor
        os.mkdir(ruta)
    
    PATH = ruta

def update_list_files():
    
    ''' Actualizar la lista de archivos a compartir que posee el servidor
        La estructura de archivos (arbol de directorio) se guardara en un json con 
        la siguiente estructura 
        
        MY_FILES = {  ARTISTA_1 :  {

                            ALBUM_1 : [  CANCION1, CANCION2 , .. CANCION N],
                            ...
                            ALBUM_N:  [  CANCION1, CANCION2 , .. CANCION N]
                            },
                    ....
                    ARTISTA_N :  {

                            ALBUM_1 : [  CANCION1, CANCION2 , .. CANCION N],
                            ...
                            ALBUM_N:  [  CANCION1, CANCION2 , .. CANCION N]
                            }
                 }    
    '''
    global MY_FILES
    artistas =  [ x for x in os.listdir(PATH) if os.path.isdir(PATH+"/"+x)] 
    for artista in artistas:

        MY_FILES[artista] = {}
        for album in os.listdir(PATH+"/"+artista):
    
            MY_FILES[artista][album] = [ x for x in os.listdir(PATH+"/"+artista+"/"+album)]

    print(" La lista de archivos compartidos ha sido actualizada\n")    

def server_start():

    print("voy a funcionar en la direccion: ",SERVER_DIR)    
    s = ctx.socket(zmq.REP)
    s.bind("tcp://*:"+PORT) # Empieza a escuchar mensajes de clientes en el puerto definido
    make_server_dir() 
    return s # Retorno el socket

def proxy_comunication():
    
    # Envio un mensaje como cliente al proxy anunciandome y entregando mi lista de archivos
    s   = ctx.socket(zmq.REQ)
    s.connect("tcp://"+IP_PROXY) #Ip del proxy

    #m = {}  Mensaje que se enviará al proxy
    m = {  "request" : "NuevosArchivos",
            "fileList" : MY_FILES,
            "myDir" : IP_SERVER
    }
    s.send_pyobj(m)
    _ = s.recv_pyobj() # Recibo confirmacion, No interesa la respuesta

if __name__ == '__main__':

    update_content()
    s = proxy_comunication()
    #registrar sockets por los cuales se va a recibir mensajess
    poll.register(s, zmq.POLLIN)
    
    while True:
        
        #print("Esperando Solicitudes")
        sockets = dict(poll.poll(1))
        if s in sockets:
            
            m = s.recv_pyobj()
            print( "Solicitud {}".format(m["request"])) # El servidor de archivos solo va a recibir solicitudes de descarga

            if m["request"] == "FileDownload":
                # Se busca  el archivo/album y se envia
                pass
            else:
                # se ignora el mensaje. Se debe responder algo para completar la comunicacion
                s.send_pyobj({"reply":"ok"})
      
    print("Esto no deberia aparecer")
    
   
    
