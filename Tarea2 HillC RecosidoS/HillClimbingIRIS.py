import GeneradorNumeros as gen
import numpy as np
import os 
Flowers = np.genfromtxt('IRIS.txt') 
solucionActual = []
mejorSolucion = []
costoActual = 0
mejorCosto = 0



def solInit():
    for i in range(150):
        solucionActual.append(gen.aleatorioEntero(3))

def inicializaCostoVecinos(costoVecino):
    for i in range(150):
        for j in range(3):
            costoVecino[i][j] = None

        
def funcionObjetivo(solucion):
    distanciaM = 0
    for i in range(149):
        for j in range(i+1,150):
            if(solucion[i]==solucion[j]):
                distanciaM += Manhattan(i,j)    
    return distanciaM

def Manhattan(i,j):
    DManhattan = abs(Flowers[j][0] - Flowers[i][0]) + abs(Flowers[j][1] - Flowers[i][1]) + abs(Flowers[j][2] - Flowers[i][2]) +abs(Flowers[j][3] - Flowers[i][3])
    return DManhattan
    
        
def generarVecinos(solucionA,costoVecino):
    valMin = 10000000000
    solucionVecino = solucionA[:]
    mejoresCostos = []  

    for i in range(150):
        aux = solucionA[i]
        for j in range(3):
            if(j!=aux):
                solucionVecino[i] = j
                costo = funcionObjetivoVecino(solucionVecino,solucionA,i)
                costoVecino[i][j] = costo
                solucionVecino[i] = aux

    for i in range(150):
        for j in range(3):
            if(costoVecino[i][j] < valMin):
                valMin = costoVecino[i][j]
                mejoresCostos.clear()
                mejoresCostos.append((i,j))
            elif(costoVecino[i][j] == valMin):
                mejoresCostos.append((i,j))

    indice = gen.aleatorioEntero(len(mejoresCostos))
    indicei, indicej = mejoresCostos[indice]
    return costoVecino[indicei][indicej],indicei, indicej
             

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
    global costoActual, mejorCosto
    costoVecino = np.zeros((150,3))
    print(solucionActual)
    print()
    file = open("data1.data","w")

    for i in range(1,31):
        """Se prepara para una nueva iteracion"""       
        inicializaCostoVecinos(costoVecino)
        recetea()

        """Se asigna una semilla"""
        gen.cambiaSemilla(i*300)
        print("Semilla", gen.semilla)



        """ Inicializa de manera aleatoria la solucion actual (arreglo solucionActual de manera global)"""
        solInit()
        costoActual = funcionObjetivo(solucionActual) #""" A esa solucion actual se le calcula su funcion objetivo (variable global)"""
        mejorSolucion = solucionActual[:] #""" Por el momento es la mejor solucion (arreglo global)"""
        mejorCosto = costoActual #""" Por el momento es el mejor costo (variable global)"""
        


        for i in range(200):    
            Cvecino,i,j = generarVecinos(solucionActual,costoVecino) #""" Para el algoritmo hillclimbing se genera sus vecinos en costos de la solucion actual """
            if(costoActual>=Cvecino):
                solucionActual[i] = j
                costoActual = Cvecino
                mejorSolucion = solucionActual[:]
                mejorCosto = costoActual
            #inicializaCostoVecinos(costoVecino)

        file.write(str(funcionObjetivo(mejorSolucion))+ os.linesep)            

    
        print(funcionObjetivo(mejorSolucion))
    
    file.close()
main()

