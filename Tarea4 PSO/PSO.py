import numpy as np
import math
import GeneradorNumeros as gen
import os



def funcionObjetivo(solucion,Flowers):
    distanciaM = 0
    for i in range(149):
        for j in range(i+1,150):
            if(solucion[i]==solucion[j]):
                distanciaM += Manhattan(i,j,Flowers)    
    return distanciaM

def Manhattan(i,j,Flowers):
    DManhattan = (abs(Flowers[j][0] - Flowers[i][0]) + abs(Flowers[j][1] - Flowers[i][1]) + abs(Flowers[j][2] - Flowers[i][2]) +abs(Flowers[j][3] - Flowers[i][3]))
    return DManhattan


def iniciaParticulas(Particulas,Flowers):
    mini = np.amin(Flowers,axis=0)
    maxi  = np.amax(Flowers,axis=0)
    for i in range(10):
        for j in range(3):
            for k in range(4):
                Particulas[i][(4*j)+k] = mini[k] + gen.aleatorio()*(maxi[k]-mini[k])




def Decodifica(Particula,Flowers):
    solucion = []
    for i in range(150):
        solucion.append(DistanciaMinima(Particula,Flowers,i))
    costo = funcionObjetivo(solucion,Flowers)
    return costo

def DistanciaMinima(Particula,Flowers,i):
    d1 = ( ((Flowers[i][0]-Particula[0])**2) + ((Flowers[i][1]-Particula[1])**2) + ((Flowers[i][2]-Particula[2])**2) + ((Flowers[i][3]-Particula[3])**2))
    d2 = ( ((Flowers[i][0]-Particula[4])**2) + ((Flowers[i][1]-Particula[5])**2) + ((Flowers[i][2]-Particula[6])**2) + ((Flowers[i][3]-Particula[7])**2))
    d3 = ( ((Flowers[i][0]-Particula[8])**2) + ((Flowers[i][1]-Particula[9])**2) + ((Flowers[i][2]-Particula[10])**2) + ((Flowers[i][3]-Particula[11])**2))

    d1 = math.sqrt(d1)
    d2 = math.sqrt(d2)
    d3 = math.sqrt(d3)
    
    if(d1<d2 and d1<d3):
        return 0
    elif(d2<d1 and d2<d3):
        return 1
    elif(d3<d2 and d3<d1):
        return 2
    

    

def main():
    Flowers = np.genfromtxt('IRIS.txt')
    Particulas =  np.zeros((10,12))
    Costo = [0,0,0,0,0,0,0,0,0,0]
    MejorPersonal = np.zeros((10,12))
    CostoPersonal = [0,0,0,0,0,0,0,0,0,0]
    MejorGlobal = []
    velocidad = np.zeros((10,12))
    c1 = 3.6
    c2 = 0.4
    
    

    
    
    file = open("data1.txt","w")
    for p in range(1,31):
        """Inicializa las particulas"""
        iniciaParticulas(Particulas,Flowers) 

        for g in range(20):        
            for i in range(10):
                Costo[i] = Decodifica(Particulas[i],Flowers)


            """Se saca el indice  de la mejor particula"""
            a = np.where(Costo == np.amin(Costo))
            indice = a[0][0]
            
            if(g==0):
                for i in range(10):
                    CostoPersonal[i] = Costo[i]
                    MejorPersonal[i] = Particulas[i]
          
                MejorGlobal = Particulas[indice]
                MejorCosto = Costo[indice]
            else:
                for i in range(10):
                    if(Costo[i]<CostoPersonal[i]):
                        MejorPersonal[i] = Particulas[i]
                        CostoPersonal[i] = Costo[i] 
                if(Costo[indice]<MejorCosto):
                    MejorCosto = Costo[indice]
                    MejorGlobal = Particulas[indice]

            for i in range(10):
                for j in range(12):
                    velocidad[i][j] += (gen.aleatorio()*c1*(MejorPersonal[i][j]-Particulas[i][j])) + (gen.aleatorio()*c2*(MejorGlobal[j]-Particulas[i][j]))
                    Particulas[i][j] += velocidad[i][j]
        
        #file.write(str(MejorCosto)+ os.linesep)
        gen.cambiaSemilla(p+1)
        print(MejorCosto)
    file.close()   
    


main()