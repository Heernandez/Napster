import zmq
import os

PROXY_DIR = "localhost:6000"
pygame.init()
ctx = zmq.Context()
def connection():
    # Conexion al proxy para solicitar listado de archivos y direccion de servidores

   s = ctx.socket(zmq.REQ)
   s.connect("tcp://"+PROXY_DIR) #direccion del proxy
   return s

def connection_2(serverDir):
    # Conexion con un determinado servidor para solicitud de archivo: formato ip:puerto

    s = ctx.socket(zmq.REQ) 
    s.connect("tcp://"+serverDir)
    return s

def lista(filesDic):

    listFile = []
    if filesDic == False:
        return []
    for key in filesDic.keys():
        for value in filesDic[key]:
            listFile.append(value)
    return listFile

if __name__ == '__main__':
    
    files = []
    while(True):

        os.system("clear")
        print("\n-----------------------\n")
        print("C/S Napster \n")
        print("1.Explorar\n")
        print("2.Descargar\n")
        print("3.Salir\n")
      
        op = int(input("Ingrese opcion: "))
        print('\n')
    
        s = connection()
        
        if op == 1:
            m = { "request" : "ListadoDeArchivos"}

            s.send_pyobj(m)
            r = s.recv_pyobj()
            '''
            if isinstance(r["reply"],dict):
                for artista in r["reply"].keys():
                    print("Artista  : {} ".format(artista))
                    for album in artista.keys():
                        print("    Album : {}".format(album))
                        for song in r[artista][album]:
                            print("        {}".format(song))
            '''
            if r["reply"] == False:

                print("No hay archivos compartidos disponibles!")

            else:
                files = lista(r["reply"])
                contador = 1
                
                for key in r["reply"].keys():
                    for value in r["reply"][key]:
                        print("{}.{}".format(contador,value))
                        contador += 1
                eleccion = int(input("Ingrese el numero del archivo que desea!"))
                    
        elif op == 2:
            if  len(files) == 0:
                    print("Aun no se ha  realizado consulta de archivos disponibles!")
                else:
            
        elif op == 3:
            s.disconnect("tcp://"+PROXY_DIR)
            break
        
        s.disconnect("tcp://"+PROXY_DIR)
