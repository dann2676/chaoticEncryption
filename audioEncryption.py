from henonClasses import Protocol, Henon
import numpy as np
import threading
import pyaudio
from time import time

#Parametros Iniciales
x1 = 0
y1 = 0
x2 = 1
y2 = 3

#Creacion de de atractores
master = Henon (x1, y1)
slave = Henon (x2, y2)

#Relacionar los actractores
sender= Protocol(master)
receiver =Protocol(slave)

#sincronizar
sender.syncrhonize (slave)


#Definicion formato de audio wav
CHUNK = 1024 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              output=True,frames_per_buffer=CHUNK) #uses default input device

#funcion que recibe array con los datos de audio y stream para reproduccion del audio.
def proceso(data, stream):

    #stream.write(data2,CHUNK)
    #print (data)

    #start_time = time.time()
    encrypt_sound = sender.encrypt(data.copy())
    #stream.write(encrypt_sound, CHUNK)
    #print encrypt_sound
    #print("--- Encrypt %s seconds ---" % (time.time() - start_time))

    #start_time = time.time()
    decrypt_sound = receiver.decrypt(encrypt_sound.copy())
    #print (decrypt_sound)
    stream.write(decrypt_sound.astype(np.int16).tostring(), CHUNK)
    #print("--- Decrypt %s seconds ---" % (time.time() - start_time))



for i in range(500): #to it a few times just to see
    start_time=time()
    data2 =stream.read(CHUNK)
    data = np.fromstring(data2, dtype=np.int16)
    print(time()-start_time)
    #proceso(data, stream)


stream.stop_stream()
stream.close()
p.terminate()
