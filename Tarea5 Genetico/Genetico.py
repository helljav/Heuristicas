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

def iniciaPoblacion(pobla, N):
    for i in range(N):
        for j in range(150):
            pobla[i][j] = gen.aleatorioEntero(3)

def barajeo(Costo, Poblacion,N):
    solucionB = []
    itera = gen.aleatorioEntero(20000)
    for i in range(itera):
        p1 = gen.aleatorioEntero(N)
        p2 = gen.aleatorioEntero(N)
        CostoB = Costo[p1]
        solucionB = Poblacion[p1][:]

        Costo[p1] = Costo[p2]
        Poblacion[p1] = Poblacion[p2][:]

        Costo[p2] = CostoB
        Poblacion[p2] = solucionB[:] 

        
def seleccionTorneo(Costo, Poblacion, N,limi,lims):
    barajeo(Costo, Poblacion,N)
    PobTorneo = np.zeros((int(N/2),150))
    CostoTorneo = [0 for x in range(int(N/2))] 
    for i in range(limi,lims):
        if(Costo[i*2]<Costo[i*2+1]):
            CostoTorneo[i] = Costo[i*2]
            PobTorneo[i] = Poblacion[i][:]
        elif(Costo[i*2]>Costo[i*2+1]):
            CostoTorneo[i] = Costo[i*2+1]
            PobTorneo[i] = Poblacion[i][:]
    return PobTorneo, CostoTorneo


def cruzaUniforme(PobTorneo1,PobTorneo2,N):
    probCruza = 0.5
    Hijos1 = np.zeros((N,150))
    Hijos2 = np.zeros((N,150))
    for i in range(N):
        for j in range(150):
            prob = gen.aleatorio()
            if(prob<probCruza):
                Hijos1[i][j] = PobTorneo2[i][j]
                Hijos2[i][j] = PobTorneo1[i][j]
            else:
                Hijos1[i][j] = PobTorneo1[i][j]
                Hijos2[i][j] = PobTorneo2[i][j]

    return Hijos1,Hijos2

def mutacion(Hijos,TazaMutacion,N):
    for i in range(N):
        prob = gen.aleatorio()
        if(prob<TazaMutacion):
            for j in range(150):
                probSR = gen.aleatorio()
                if(probSR<0.5):
                    Hijos[i][j] += Hijos[i][j]
                    if(Hijos[i][j]==3):
                        Hijos[i][j] = 0
                else:
                    Hijos[i][j] -= Hijos[i][j]
                    if(Hijos[i][j]==-1):
                        Hijos[i][j] = 2 

def ordenaPoblacion(Poblacion,Costos,N):
    PoblacionAux = []
    for i in range(1,N):
        for j in range(0,N-i):
            if(Costos[j] > Costos[j+1]):
                k = Costos[j+1]
                PoblacionAux = Poblacion[j+1]

                Costos[j+1] = Costos[j]
                Poblacion[j+1] = Poblacion[j][:]

                Costos[j] = k;
                Poblacion[j] = PoblacionAux[:]

    

    

def main():
    """Tamaño de la poblacion sera 20, 10 segeneran de forma aleatoria y los demas 10 por torneo"""
    N = 60
    TazaMutacion = 0.01

    Poblacion = np.zeros((N,150))
    Costo = [0 for x in range(N)]
    Flowers = np.genfromtxt('IRIS.txt')
    

    

    for i in range(30):
        """Solo iniciamos la mitad de la poblacion total"""
        iniciaPoblacion(Poblacion,int(N/2))
    
        """Sacamos los costos de esa poblacion inicial"""
        for i in range(int(N/2)):
            Costo[i] = funcionObjetivo(Poblacion[i],Flowers)


        for i in range(10):
            """Hacemos 2 torneos"""
            """Le pasamos la poblacion para que la baraje, solo lo hara con los primeros 10 mejores"""
            """Posteriormente se seleccionaran a los 5 mejores y los regreszara y sus costos"""
            PobTorneo1, CostoTorneo1 = seleccionTorneo(Costo,Poblacion,int(N/2),0,int(N/4))
            PobTorneo2, CostoTorneo2 = seleccionTorneo(Costo,Poblacion,int(N/2),0,int(N/4))

            """Realizamos la cruza uniforme y nos va a salir 10 hijos en total"""
            Hijos1 , Hijos2 = cruzaUniforme(PobTorneo1,PobTorneo2,int(N/4))
            
            mutacion(Hijos1,TazaMutacion,int(N/4))
            mutacion(Hijos2,TazaMutacion,int(N/4))

            """Sacamos los costos de esa poblacion Hijos1"""
            for i in range(int(N/2),int(N/2 + N/4)):
                Costo[i] = funcionObjetivo(Hijos1[i-int(N/2)],Flowers)
                Poblacion[i] = Hijos1[i-int(N/2)][:]
            
            """Sacamos los costos de esa poblacion inicial"""
            for i in range(int(N/2 + N/4),N):
                Costo[i] = funcionObjetivo(Hijos2[i-int(N/2 + N/4)],Flowers)
                Poblacion[i] = Hijos2[i-int(N/2 + N/4)][:]

            ordenaPoblacion(Poblacion,Costo,N)

        print(Costo[0])
        gen.cambiaSemilla(i+1)
        Costo = [0 for x in range(N)]
        Poblacion = np.zeros((N,150))
        

    

    
   
    
    

main()