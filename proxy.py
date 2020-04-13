import zmq
import random
import json

# Variables Globales -----------------------------------
CLIENT_PORT = "6000" # Puerto por el que se atienden clientes y nuevos servidores
DIC = {} # Directorio de Archivos compartidos
ctx = zmq.Context() # Contexto para creacion de sockets
SHARED_FILES = {} # Diccionario de contenido asociado a cada servidor

# ---------------------------------------------------------
def client_connection():
    # Se crea el socket que estara escuchando clientes
    sc   = ctx.socket(zmq.REP)
    sc.bind("tcp://*:"+CLIENT_PORT) # El socket empieza a escuchar en el puerto
    return sc

if __name__ == '__main__':

    #global SHARED_FILES
    print("Napster is starting at port 6000 ....\nListening .....")
    s = client_connection()

    while True:
        print("..Esperando solicitudes...")
        m = s.recv_pyobj()
        print("Solicitud : {} ".format(m["request"]))
        if ( m["request"] == "ListadoDeArchivos" ):

            # Solicitud de un cliente para conocer los archivos disponibles
            if len(SHARED_FILES) != 0:

                s.send_pyobj({"reply":SHARED_FILES})
            else:

                s.send_pyobj({"reply": False})

        elif ( m["request"] == "NuevosArchivos" ):
            #Solicitud de un nuevo servidor anunciando sus archivos
            print(" Estoy recibiendo ",m)
            SHARED_FILES[m["myDir"]] = m["fileList"]
            s.send_pyobj({"reply":"ok"})

        else:
            #Ignorar mensaje. Se debe responder algo para completar la comunicacion
            s.send_pyobj({"reply":"ok"})
 
       