import numpy as np
import math
import GeneradorNumeros as gen
import os
Flowers = np.genfromtxt('IRIS.txt')
Feromonas = np.zeros((150,3))
Distancia = np.zeros((150,3))
for i in range(150):
    for j in range(3):
        Feromonas[i][j] = 10

Centros = []

def minMaxFlowers(j):
    Auxmin = 1000000000000
    Auxmax = -100000000000
    for i in range(150):
        if(Flowers[i][j]<Auxmin):
            Auxmin = Flowers[i][j]
        if(Flowers[i][j]>Auxmax):
            Auxmax = Flowers[i][j]
    return Auxmin,Auxmax

        

def initCentroides(Centros):
    min1, max1 = minMaxFlowers(0)
    min2, max2 = minMaxFlowers(1)
    min3, max3 = minMaxFlowers(2)
    min4, max4 = minMaxFlowers(3)
    for k in range(3):
        u1 = gen.aleatorio()
        u2 = gen.aleatorio()
        u3 = gen.aleatorio()
        u4 = gen.aleatorio()        
        Centros.append([min1 + u1*(max1-min1), min2 + u2*(max2-min2),min3 + u3*(max3-min3),min4 + u4*(max4-min4)])
    

def Euclides(i,j):
    dis = 0
    centro = Centros[j]
    for k in range(4):
        dis += (Flowers[i][k]-centro[k])**2
    return math.sqrt(dis) 
    
def distancia(Distancia):
    for i in range(150):
        for j in range(3):
            Distancia[i][j] = Euclides(i,j)



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

def Iniciahormigas():
    q0 = 0.8
    solucion = []
    for i in range (150):
        u = gen.aleatorio()
        if(u<q0):
            solucion.append(argumentoMax(i))
        else:
            r = gen.aleatorio()
            if(r<(Feromonas[i][0]/(Feromonas[i][0]+Feromonas[i][1]+Feromonas[i][2]))):
                solucion.append(0)
            elif(r<((Feromonas[i][0]+Feromonas[i][1])/(Feromonas[i][0]+Feromonas[i][1]+Feromonas[i][2]))):
                solucion.append(1)
            else:
                solucion.append(2)

    costo = funcionObjetivo(solucion)
    return solucion,costo
    
def argumentoMax(i):
    auxMaximo = -10000000000
    for j in range(3):
        comp = (Feromonas[i][j]/Distancia[i][j])
        if(auxMaximo<comp):
            auxMaximo = comp
            indice = j
    return indice

""" Devuelve el indice con el menor costo de las 5 hormigas que estamos poniendo"""
def menorCostoHormiga(costo):
    auxMenos = 1500000000
    for i in range(len(costo)):
        if(costo[i]<auxMenos):
            auxMenos = costo[i]
            indice = i
    return int(indice)

""" Primera actualizacion de la feromona"""
def actualizaFeromona():
    TazaE = 0.8 
    for i in range(150):
        for j in range(3):
            Feromonas[i][j] = Feromonas[i][j]*(1-TazaE) 

def reseteaCentroide(Centroide):
    for i in range(3):
        for j in range(4):
            Centroide[i][j] = 0 
    # for i in range(3):
    #     Centroide[i] = [0,0,0,0] 



              

def main():
    
    Hormigas = []
    Costo =  []
    


    for i in range(0,30):
        initCentroides(Centros)               
        constoMejor = 1000000000000000
        distancia(Distancia)
        Hormigas.clear()
        Costo.clear()    
                

        for i in range(80):

            """ INICIAMOS A NUESTRAS HORMIGAS"""
            for i in range(5):
                hormi, costo = Iniciahormigas()
                Hormigas.append(hormi)
                Costo.append(costo)

            
            # print(Hormigas)

            """ SACAMOS LA HORMIGA CON EL MENOR COSTO """
            mejorHormiga = menorCostoHormiga(Costo)

            """ Primera actualizacion de la feromona base a la taza de evaporacion a toda la matriz de la Feromona"""
            actualizaFeromona()

            """Segunda Actualizacion de la feromona"""
            for i in range(150):
                Feromonas[i][Hormigas[mejorHormiga][i]] += (10000/Costo[mejorHormiga])
            
            
            """ Se resetea los centroides"""
            reseteaCentroide(Centros)

            contador = np.array([0,0,0])
            """Actualizamos centros"""
            for i in range(150):
                cluster = Hormigas[mejorHormiga][i]
                for k in range(4):
                    Centros[cluster][k] += Flowers[i][k]
                    contador[cluster] += 1

            for i in range(3):
                for j in range(4):
                    if(contador[i]>0):
                        Centros[i][j] = Centros[i][j]/contador[i]
                    else:
                        Centros[i] = [0,0,0,0]
            

            if(Costo[mejorHormiga]<constoMejor):
                constoMejor = Costo[mejorHormiga]
        print(costo)        
        gen.cambiaSemilla(i+1)
        
        
        
        
    
    
    
    
    


   
    

    
    
     

    
    
     
        
        

main()