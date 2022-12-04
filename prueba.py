import numpy as np
import tensorflow as tf
import json
import sys

longitud, altura = 100, 100

if sys.argv[2] == 'modeloA_1.h5':
    longitud,altura = 100,100
else:
    longitud,altura = 125,125

modelo = f'./Perros/modelo/{sys.argv[2]}'
pesos = f'./Perros/modelo/{sys.argv[2]}'
cnn = tf.keras.models.load_model(modelo)
cnn.load_weights(pesos)

with open('clases.json') as json_file:
    clases = json.load(json_file)

x = tf.keras.preprocessing.image.load_img(sys.argv[1], target_size=(longitud,altura))
x = tf.keras.preprocessing.image.img_to_array(x)
x = np.expand_dims(x,axis=0)
arreglo = cnn.predict(x)
resultado = np.argmax(arreglo)
print((list(clases.keys())[list(clases.values()).index(resultado)]))