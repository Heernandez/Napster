import zmq
import random
import json

# Variables Globales -----------------------------------
CLIENT_PORT = "6000" # Puerto por el que se atienden clientes y nuevos servidores
DIC = None # Directorio de Archivos compartidos
ctx = zmq.Context() # Contexto para creacion de sockets
SHARED_FILES = {}
# ---------------------------------------------------------

def client_connection():
    # Se crea el socket que estara escuchando clientes
    sc   = ctx.socket(zmq.REP)
    sc.bind("tcp://*:"+CLIENT_PORT) # El socket empieza a escuchar en el puerto
    return sc

if __name__ == '__main__':

    global SHARED_FILES
    print("Napster is starting at port 6000 ....\nListening .....")
    s = client_connection()
    #registrar sockets por los cuales se va a recibir mensajes
    poll.register(s, zmq.POLLIN)
    while True:

        m = s.recv_pyobj()
        print("Solicitud : {} ".format(m["request"]))

        if ( m["request"] == "ListadoDeArchivos" ):
            # Solicitud de mostrar que archivos hay
            pass
            
        elif ( m["request"] == "Direccion"):
            pass
        
        elif ( m["request"] == "NuevosArchivos" ):
            
            SHARED_FILES[m["myDir"]] = m["fileList"]
            s.send_pyobj({"reply":"ok"})

        else:
            #Ignorar mensaje. Se debe responder algo para completar la comunicacion
            s.send_pyobj({"reply":"ok"})
 
       