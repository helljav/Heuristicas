import numpy as np
import math
import GeneradorNumeros as gen
import os
Flowers = np.genfromtxt('IRIS.txt') 
solucionActual = []
mejorSolucion = []
costoActual = 0
mejorCosto = 0



def solInit():
    for i in range(150):
        solucionActual.append(gen.aleatorioEntero(3))


        
def funcionObjetivo(solucion):
    distanciaM = 0
    for i in range(149):
        for j in range(i+1,150):
            if(solucion[i]==solucion[j]):
                distanciaM += Manhattan(i,j)    
    return distanciaM

def Manhattan(i,j):
    DManhattan = (abs(Flowers[j][0] - Flowers[i][0]) + abs(Flowers[j][1] - Flowers[i][1]) + abs(Flowers[j][2] - Flowers[i][2]) +abs(Flowers[j][3] - Flowers[i][3]))
    return DManhattan
        
def generarVecino(solucionA):
    solucionVecino = solucionA[:]
    i = gen.aleatorioEntero(150)
    u = gen.aleatorio()
    if(u<0.5):
        solucionVecino[i] = solucionVecino[i] +1
        if(solucionVecino[i]>2):
            solucionVecino[i] = 0
    else:
        solucionVecino[i] = solucionVecino[i] - 1 
        if (solucionVecino[i]<0):
            solucionVecino[i] = 2

    costoVecino = funcionObjetivoVecino(solucionVecino,solucionA,i)

    return solucionVecino,costoVecino

    
    
             

def funcionObjetivoVecino(solucionVecino,solucionA,indice):
    global costoActual
    costo = costoActual
    for j in range(150):
        if(solucionA[indice] == solucionA[j] and indice != j):
            costo -= Manhattan(indice,j)
    for j  in range(150):
        if(solucionVecino[indice] == solucionVecino[j] and indice != j):
            costo += Manhattan(indice,j)
    return costo

def recetea():
    global costoActual, mejorCosto, mejorSolucion, solucionActual
    solucionActual.clear()
    mejorSolucion.clear()
    costoActual = 0
    mejorCosto = 0

def main():
    global costoActual, mejorCosto,solucionActual

    file = open("data2.data","w")

    for i in range(1,31):
        """Se prepara para una nueva iteracion"""       
        recetea()

        """Se asigna una semilla"""
        gen.cambiaSemilla(i*300)
        print("Semilla", gen.semilla)

        """ Inicializa de manera aleatoria la solucion actual (arreglo solucionActual de manera global)"""
        solInit()
        costoActual = funcionObjetivo(solucionActual) #""" A esa solucion actual se le calcula su funcion objetivo (variable global)"""
        mejorSolucion = solucionActual[:] #""" Por el momento es la mejor solucion (arreglo global)"""
        mejorCosto = costoActual #""" Por el momento es el mejor costo (variable global)"""
        temp = 100
        tempFria = 0.001
        nIteraciones = 200
        alfa = 0.95
        


        """Inicia lo chido"""

        while(temp>tempFria):
            for i in range(nIteraciones):
                solucionVecino, costoVecino = generarVecino(solucionActual)
                if(costoVecino<= costoActual):
                    solucionActual = solucionVecino[:]
                    costoActual = costoVecino
                    if(costoActual<mejorCosto):
                        mejorSolucion = solucionActual[:]
                        mejorCosto = costoActual
                else:
                    u = gen.aleatorio()
                    b = math.exp((costoActual-costoVecino)/temp)
                    if(u<b):
                        solucionActual = solucionVecino[:]
            temp = temp*alfa

        fo = funcionObjetivo(mejorSolucion)
        file.write(str(fo)+ os.linesep)
        print(fo)

    file.close()
main()

