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
PROXY_DIR = "localhost:6000"
PORT = "5555"
SERVER_DIR = getIp()+":"+PORT #Direccion en la que esta el servidor actual( se debe cambiar el puerto para cada servidor ejecutado en la misma maquina)
# ------------------------------------------------------
def update_list_files():
    
    #Actualizar la lista de archivos a compartir que posee el servidor   
    global MY_FILES
    MY_FILES = [x for x in os.listdir(PATH)]
    print(" La lista de archivos compartidos ha sido actualizada\n")    

def server_start():

    print("voy a funcionar en la direccion: ",SERVER_DIR)    
    ss = ctx.socket(zmq.REP)
    ss.bind("tcp://*:"+PORT) # Empieza a escuchar mensajes de clientes en el puerto definido
    # Se crea la carpeta del servidor inicialmente vacia, a la cual se cargaran los archivos a compartir
    # Si ya existe la carpeta no se hace nada
    global PATH
    directorio = os.getcwd() # Directorio actual
    carpeta = "/provider"    # nombre de la carpeta que contiene los archivos a compartir ( debe estar en la misma carpeta de server.py)
    PATH = directorio+carpeta
    return ss # Retorno el socket

def proxy_comunication():
    
    update_list_files()
    # Envio un mensaje como cliente al proxy anunciandome y entregando mi lista de archivos
    s   = ctx.socket(zmq.REQ)
    s.connect("tcp://"+PROXY_DIR) #Ip del proxy

    #m = {}  Mensaje que se enviará al proxy
    m = {  "request" : "NuevosArchivos",
            "fileList" : MY_FILES,
            "myDir" : SERVER_DIR
    }
    print("Yo envio ",m)
    s.send_pyobj(m)
    _ = s.recv_pyobj() # Recibo confirmacion, No interesa la respuesta
    s.disconnect("tcp://"+PROXY_DIR) #finaliza la conexion

if __name__ == '__main__':

    ss = server_start() # Inicio el servidor
    proxy_comunication()

    while True:
        
        print("...Esperando Solicitudes...")
        m = ss.recv_pyobj()
        print( "Solicitud {}".format(m["request"])) # El servidor de archivos solo va a recibir solicitudes de descarga
        if m["request"] == "FileDownload":
                
            lista = os.listdir(PATH)
            aux =  m["name"] 
            if aux in lista:
                with open(PATH+'/'+aux,'rb') as f:
                    file = f.read()
                    ss.send_pyobj({"reply":file,"name":aux})
                    f.close()
            else:
                ss.send_pyobj({"reply":False})
        else:
            # se ignora el mensaje. Se debe responder algo para completar la comunicacion
            ss.send_pyobj({"reply":"ok"})
      
    print("Esto no deberia aparecer")
    
   
    
