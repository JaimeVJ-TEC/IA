import sys
import os
import tensorflow as tf
from tensorflow_core.python.keras import optimizers,layers
from tensorflow_core.python.keras.models import Sequential
from tensorflow_core.python.keras.layers import Dropout,Flatten,Dense,Activation,Convolution2D,MaxPooling2D
from tensorflow_core.python.keras import backend as k
import json

k.clear_session()

#Rutas del dataset y del modelo
modelo = './Perros/modelo/modeloA_1.h5'
data_entrenamiento = "./Perros/data/entrenamiento"
data_validacion ="./Perros/data/validacion"


#Red Neuronal
epocas  = 20                    #Una epoca es un ciclo completo entre los datos de entrenamiento
altura, longitud = 100,100      #Height y Widht de las imagenes
batch_size = 100                #
pasos = 100                     #Un paso es una actualizacion gradiente
pasos_validacion = 100

#Filtros convolucionales
"""
Filtro o capa convolucional: En esta capa preservamos la relación espacial entre los píxeles aprendiendo las características 
de la imagen usando pequeños cuadrados de datos de entrada. 
Estos cuadrados de datos de entrada también se denominan filtros o núcleos. 
La matriz formada al deslizar el filtro sobre la imagen y calcular el producto escalar se denomina mapa de características. 
Cuantos más filtros tengamos, más características de la imagen se extraerán y mejor será nuestra red para reconocer patrones
en imágenes invisibles.
"""
filtroConv = 32 
filtroConv2 = 64
tamano_filtro = (3,3)
tamano_filtro2 = (3,3)
tama_pol = (2,2)
clases = 16
lr = 0.0005 #longitud de la neurona

# Pre-procesamiento de imagenes
entrenamiento_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.3,          #Augmentacion de datos
    zoom_range = 0.3,           #Augmentacion de datos
    horizontal_flip = True      #Augmentacion de datos
)

validacion  = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale = 1./255
)

imagen_entrenamiento = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size = (altura,longitud),
    batch_size = batch_size,
    class_mode = "categorical"
)

imagen_validacion = validacion.flow_from_directory(
    data_validacion, 
    target_size = (altura,longitud),
    batch_size = batch_size,
    class_mode = "categorical"
)

generator= entrenamiento_datagen.flow_from_directory(data_entrenamiento, batch_size=batch_size)
label_map = (generator.class_indices)
with open("clases.json","w") as write_file:
    json.dump(label_map,write_file)


#CNN

"""La API del modelo Sequential es una forma de crear modelos de aprendizaje profundo 
donde se crea una instancia de la clase Sequential y se crean y agregan capas de modelo."""
cnn = Sequential()  
#cnn = tf.keras.models.load_model(modelo)

#1ra Capa de nuestra red neuronal.
cnn.add(Convolution2D(filtroConv,tamano_filtro, padding="same",input_shape=(altura,longitud,3),activation='relu'))
cnn.add(MaxPooling2D(pool_size = tama_pol))
#2da Capa
cnn.add(Convolution2D(filtroConv2,tamano_filtro2, padding="same",input_shape=(altura,longitud,3),activation='relu'))
cnn.add(MaxPooling2D(pool_size = tama_pol))

cnn.add(Flatten())
cnn.add(Dense(256,activation='relu'))
cnn.add(Dropout(0.5))

cnn.add(Dense(clases,activation='softmax'))

#Para porder crear nuestra IA
cnn.compile(loss='categorical_crossentropy',optimizer = optimizers.adam_v2.Adam(lr=lr), metrics=['accuracy'])

cnn.fit(imagen_entrenamiento,steps_per_epoch = pasos, epochs = epocas, validation_data = imagen_validacion, validation_steps = pasos_validacion)


#Aqui es donde guardamos nuestro modelo
dir = "./Perros/modelo"

if not os.path.exists(dir):
    os.mkdir(dir)
    
cnn.save('./Perros/modelo/modeloA_1.h5')