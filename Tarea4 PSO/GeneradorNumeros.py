import math
a = 314159269
c = 453806245
semilla = 1
modulo = math.pow(2,31)

def cambiaSemilla(i):
    global semilla
    semilla = i

def aleatorio():
    global semilla
    semillaDesp = (a*semilla + c) % modulo
    semilla = semillaDesp
    return semilla/modulo


def aleatorioEntero(N):
    global semilla
    semillaDesp = (a*semilla + c) % modulo
    semilla = semillaDesp
    rango = (int) ((semilla/modulo)*N)
    if(rango == N):
        rango = N-1
    return rango
