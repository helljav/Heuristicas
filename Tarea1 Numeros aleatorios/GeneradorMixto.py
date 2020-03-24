import math
import os
a = 314159269
c = 453806245
semilla = 1
modulo = math.pow(2,31) 
arregloSemilla = []
def aleatorio():
    global semilla
    semillaDesp = (a*semilla + c) % modulo
    semilla = semillaDesp
    return semilla/modulo

def cambiaSemilla(i):
    global semilla
    semilla = i
def main():
    file = open("data1.data","w")
    
    for i in range(500):
        file.write(str(aleatorio())+" "+str(aleatorio())+ os.linesep)
    
    file.close()
