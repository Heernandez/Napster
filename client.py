import zmq
import os
import pygame 
pygame.mixer.pre_init(44100, -16, 2, 2048) 

pygame.init()
ctx = zmq.Context()

def connection():

   s = ctx.socket(zmq.REQ)
   s.connect("tcp://localhost:6000") #direccion del proxy

   return s

def connection_2(PORT):

    s = ctx.socket(zmq.REQ) 
    s.connect("tcp://localhost:"+PORT)

    return s

if __name__ == '__main__':
    
    
    
    while(True):
        os.system("clear")
        print("\n-----------------------\n")
        print("C/S MusicPlayer \n")
        print("1.Pistas\n")
        print("2.Cerrar\n")
      
        op = int(input("Ingrese opcion: "))

        print('\n')
        
        s = connection()
        
        if op == 1:
            s.send_multipart([b'2'])
            msg = s.recv_multipart()
            indice = 1
            for i in msg:
                print (str(indice)+'.'+i.decode('utf-8'))
                indice+=1
            
            resp = int(input("Ingrese el numero de la cancion a reproducir o cero (0) para regresar"))
            if resp == 0:       
                x = input("presione una tecla ---")
            else:
                
                aux = msg[resp-1]
                print("Has Elegido :",aux.decode('utf-8'))
                
                nombre = os.path.splitext(aux.decode('utf-8'))[0]
                
                s.send_multipart([b'3',aux])
                m = s.recv_multipart()

                k = 1

                try:
                    os.remove('temp.mp3')
                except:
                    print("") 
                
                
                for i in m:
                    s = connection_2(i.decode('utf-8'))
                    nombrebuscar = nombre + str(k)
                    s.send_multipart([b'escuchar',nombrebuscar.encode()])
                
                    a = s.recv_multipart()
                    with open('temp.mp3','ab') as f:
                        f.write(a[0])
                        f.close()
                        
                    k+=1
                    

                
                pygame.mixer.music.load('temp.mp3')
                pygame.mixer.music.play()
                
                while True:
                    x = input('presione cero (0) para detener la reproduccion')
                    if x == '0':
                        break
                pygame.mixer.music.stop()
                os.remove('temp.mp3')
       
        elif op == 2:
            break
