import zmq
import os
from pygame import mixer
#pygame.mixer.pre_init(44100, -16, 2, 2048)  Active esta linea si hay errores en la reproduccion
mixer.init()

PROXY_DIR = "localhost:6000"
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

        #os.system("cls") #aplica para windows
        print("\n-----------------------\n")
        print("C/S Napster \n")
        print("1.Explorar\n")
        print("2.Descargar\n")
        print("3.Salir\n")
      
        op = int(input("Ingrese opcion: "))
        print('\n')
    
        s = connection()
        
        if op == 1:

            s.send_pyobj({ "request" : "ListadoDeArchivos"})
            r = s.recv_pyobj()
            if r["reply"] == False:

                print("No hay archivos compartidos disponibles!")
            else:
                
                files = lista(r["reply"])
                contador = 1
                for key in r["reply"].keys():
                    for value in r["reply"][key]:
                        print("{}.{}".format(contador,value))
                        contador += 1    
                _ = input("Presione una tecla para continuar")    
        elif op == 2:
            if  len(files) == 0:
                    _ = input("Aun no se ha  realizado consulta de archivos disponibles!..\nPresione una tecla para continuar")
                    #os.system("Pause") # Aplica en windows ... 
            else:
                eleccion = int(input("Ingrese el numero del archivo que desea!"))
                if (eleccion > 0 and eleccion <= len(files)):
                        
                    for key in r["reply"].keys():
                                
                        for value in r["reply"][key]:
                            
                            if value == files[eleccion]:
                                print("Le dire al servidor en ",key)
                                server = connection_2(key)
                                server.send_pyobj({"request":"FileDownload","name":value})
                                song = server.recv_pyobj()
                                server.disconnect("tcp://"+key)
                                
                                #aqui guardo el archivo y tambien se puede iniciar la reproduccion si se desea con alguna libreria
                                if song["reply"] == False:
                                    print("Es posible que el archivo haya sido eliminado del servidor!")
                                else:
                                    with open(song["name"],'ab') as f:
                                        f.write(song["reply"])
                                        f.close()
                                    
                                    #Reproducir
                                    mixer.music.load(song["name"]) # si no funciona entonces poner os.getcwd()+"/"+song["name"]
                                                                       
                                    while True:
                                        x = input('presione cero (0) para detener la reproduccion')
                                        if x == '0':
                                            break
                                    pygame.mixer.music.stop()
                                    #os.remove('temp.mp3') Active esta linea si desea hacer creeer al usuario que no descargo sino que reprodujo en linea solamente
                                break
                else:
                    print("La eleccion no coincide con ningun archivo!")
        elif op == 3:
            s.disconnect("tcp://"+PROXY_DIR)
            break
        
        s.disconnect("tcp://"+PROXY_DIR)
