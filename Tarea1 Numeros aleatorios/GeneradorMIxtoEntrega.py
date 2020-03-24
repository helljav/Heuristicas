import math
a = 314159269
c = 453806245
semilla = 1
modulo = math.pow(2,31) - 1
arregloSemilla = []
arregloSemilla.append(semilla)
def aleatorio(N):
    global semilla
    semillaDesp = (a*semilla + c) % modulo
    semilla = semillaDesp
    arregloSemilla.append(semilla)
    rango = (int) ((semilla/modulo)*N)
    if(rango == 0):
        rango = 0
    elif(rango == N):
        rango = N-1
    return rango

def main():
    N = 0
    opcion = 0
    print()
    while(True):
        print("\n¿Deseas un numero aleatorio de  0 a N-1?")
        opcion = int(input("1.-SI     2.-No :") )
        if(opcion == 2):
            break
        N = int(input("Dame el valor de N entero :"))
        print(aleatorio(N))
main()