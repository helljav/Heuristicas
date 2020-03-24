#linea de comando
#instalar numpy; scipy; matplotlib; sklearn; tensorflow; IPython
#Usar el siguiene ejemplo
#pip install numpy
#error con tensorflow : module 'tensorflow' has no attribute 'placeholder'
##Instalé Anaconda
#desinstalé tensorflow
# Lo volví a instalar con anaconda: conda install tensorflow

import numpy as np
import scipy as sc

from sklearn.datasets import make_circles

import copy
archivo= open ('Circulos_Concentricos.txt','r')
lineas = len(open('Circulos_Concentricos.txt').readlines())

datos=[]
datosX=[]
datosY=[]
for i in range(lineas):
    dato=archivo.readline().split(',')
    datos.append(dato)
for j in range(lineas):
    d1 = []
    for k in range(2):
        d = float(datos[j][k])
        d1.append(d)
    datosX.append(d1)
    d = int(datos[j][2])
    datosY.append(d)

print('X', datosX[0], 'X', datosX[1], 'Y', datosY[0])
# Creamos nuestros datos artificiales, donde buscaremos clasificar
# dos anillos concéntricos de datos.
# 250 puntos en cada círculo
# X : array of shape [n_samples, 2]... The generated samples.
# Y : array of shape [n_samples]... The integer labels (0 or 1) for class membership of each sample.

#X, Y = make_circles(n_samples=500, factor=0.25, noise=0.05)

X = np.array(datosX)
Y = np.array(datosY)
# Resolución del mapa de predicción.
res = 100

# Coordendadas del mapa de predicción.
_x0 = np.linspace(-1.5, 1.5, res)
_x1 = np.linspace(-1.5, 1.5, res)

# Input con cada combo de coordenadas del mapa de predicción.
_pX = np.array(np.meshgrid(_x0, _x1)).T.reshape(-1, 2)

# Objeto vacio a 0.5 del mapa de predicción.
_pY = np.zeros((res, res)) + 0.5

#___________________
#___________________
#___________________
#___________________

import tensorflow as tf

# Definimos los puntos de entrada de la red, para la matriz X e Y.
iX = tf.placeholder('float', shape=[None, X.shape[1]])
iY = tf.placeholder('float', shape=[None])

nn = [2, 3, 3, 1]  # número de neuronas por capa.
#nn = [2, 3, 1]  # número de neuronas por capa.

# Capa 1
W1 = tf.Variable(tf.random_normal([nn[0], nn[1]]), name='Weights_1')
b1 = tf.Variable(tf.random_normal([nn[1]]), name='bias_1')

l1 = tf.nn.relu(tf.add(tf.matmul(iX, W1), b1))
#l1 = tf.nn.sigmoid(tf.add(tf.matmul(iX, W1), b1))

# Capa 2
W2 = tf.Variable(tf.random_normal([nn[1], nn[2]]), name='Weights_2')
b2 = tf.Variable(tf.random_normal([nn[2]]), name='bias_2')

l2 = tf.nn.relu(tf.add(tf.matmul(l1, W2), b2))
#l2 = tf.nn.sigmoid(tf.add(tf.matmul(l1, W2), b2))

#W2 = tf.Variable(tf.random_normal([nn[1], nn[2]]), name='Weights_2')
#b2 = tf.Variable(tf.random_normal([nn[2]]), name='bias_2')


# Capa 3
W3 = tf.Variable(tf.random_normal([nn[2], nn[3]]), name='Weights_3')
b3 = tf.Variable(tf.random_normal([nn[3]]), name='bias_3')

# Vector de predicciones de Y.
pY = tf.nn.sigmoid(tf.add(tf.matmul(l2, W3), b3))[:, 0]
#pY = tf.nn.sigmoid(tf.add(tf.matmul(l1, W2), b2))[:, 0]

# Evaluación de las predicciones.
loss = tf.losses.mean_squared_error(pY, iY)

# Definimos al optimizador de la red, para que minimice el error.
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(loss)

n_steps = 8000 # Número de ciclos de entrenamiento.

t = tf.trainable_variables()# Aquí guardamos los pesos y sesgos

with tf.Session() as sess:

  # Inicializamos todos los parámetros de la red, las matrices W y b.
  sess.run(tf.global_variables_initializer())
  tvars_vals = sess.run(t)

  # Iteramos n pases de entrenamiento.
  for step in range(n_steps):

    # Evaluamos al optimizador, a la función de coste y al tensor de salida pY.
    # La evaluación del optimizer producirá el entrenamiento de la red.
    #sess.run you will run the tensorflow graph and the function will return a tuple
    # of the value of the variables or ops you specified in the list input
    # The optimizer returns nothing, and so the first tuple value is _
    # the second value returns loss.

    _, _loss, _pY = sess.run([optimizer, loss, pY], feed_dict={ iX : X, iY : Y })

    # You can ask for any value in the tensorflow graph anywhere along the way
    # if you want to get the value of an intermediate layer output.
    # Just add that op or variable to the input list to sess.run.

    # Cada 200 iteraciones, imprimimos métricas.
    if step % 200 == 0:

      # Cálculo del accuracy.
      acc = np.mean(np.round(_pY) == Y)

      # Impresión de métricas.
      print('Step', step, '/', n_steps, '- Loss = ', _loss, '- Acc =', acc)

    #print("Weight matrix: {0}".format(sess.run(t[3])))
#  tvars_vals = sess.run(t)
for var, val in zip(t, tvars_vals):
    print(var.name, val)
