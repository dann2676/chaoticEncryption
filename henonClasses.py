import numpy as np
import time
class Henon:
    def __init__(self, x, y):
        self.a= 1.4
        self.b =0.3
        self.c =0.8
        self.x = x
        self.y = y
    def getX(self, x, y):
        return self.a+self.b*y-x**2
    def getY(self, x, y):
        return x
    def getXY(self):
        x=self.a+self.b*self.y-self.x**2
        self.y=self.x
        self.x=x
        return self.x, self.y
    def getX_sych(self, x, y, x2):
        return self.getX(x, y)+self.c*((x**2)-(x2**2))
    

class Protocol:
    def __init__(self, maestro):
        self.maestro=maestro
        
    def getSequence(self, length):
        sequence=[]
        x, y=self.maestro.x,self.maestro.y
        sequence.append(x)
        for i in range(length-1):
            x, y= self.maestro.getXY()
            sequence.append(x)
        self.maestro.x,self.maestro.y=x, y
        return np.array(sequence)
    
    def syncrhonize (self, esclavo):
        x1 =self.maestro.x
        y1 =self.maestro.y
        x2 =esclavo.x
        y2 =esclavo.y
        while (x1-x2)!=0 or (y1-y2)!=0:
            x1_n= self.maestro.getX(x1, y1)
            y1_n= self.maestro.getY(x1, y1)
            x2_n= esclavo.getX_sych(x2, y2, x1)
            y2_n= esclavo.getY(x2, y2)
            x1, y1, x2, y2=x1_n, y1_n, x2_n, y2_n
        self.maestro.x=x1
        self.maestro.y=y1
        esclavo.x=x2
        esclavo.y=y2
                
    def permute(self, sound, sequence, code):
        for i in range (len(sequence)):
            sound = np.roll(sound, int(sequence[i])*code, axis=0)
        return sound
    
    def diffusion(self, sound, sequence, code):
        sound = sound + (code*sequence)
        return sound
    
    def encrypt(self, sound):
        sequence = np.rint(self.getSequence(len(sound))*1000)
        sound = self.diffusion(sound, sequence, 1)
        sound = self.permute(sound, sequence, 1)
        return sound
    
    def decrypt(self, sound):
        sequence = np.rint(self.getSequence(len(sound))*1000)
        sound = self.permute(sound, sequence, -1)
        sound = self.diffusion(sound, sequence, -1)
        return sound
