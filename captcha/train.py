import os
import glob

import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import *

from common import *


LETTER_IMAGES_FOLDER = "extracted"
MODEL_FILENAME = "model.tflite"


# initialize the data and labels
data = []
labels = []

# loop over the input images
for img_file in glob.glob(os.path.join(LETTER_IMAGES_FOLDER, "*/*.png")):
    label = img_file.split(os.path.sep)[-2]
    img = Image.open(img_file)
    img = img.resize((20, 20))

    img = np.array(img)
    # Add a third channel dimension to the image to make Keras happy
    img = np.expand_dims(img, axis=2)

    data.append(img)
    labels.append(label2id(label))


data = np.array(data, dtype=np.float32)
labels = np.array(labels, dtype=np.int)

(X_train, X_test, Y_train, Y_test) = train_test_split(
    data, labels, test_size=0.25, random_state=0)
Y_train = get_one_hot(Y_train, nb_classes)
Y_test = get_one_hot(Y_test, nb_classes)

model = Sequential()
model.add(Conv2D(32, 3, padding="same",
                 input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(64, 3, padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dense(nb_classes, activation="softmax"))

model.compile(loss="categorical_crossentropy",
              optimizer="adam", metrics=["accuracy"])

model.fit(X_train, Y_train, validation_data=(
    X_test, Y_test), batch_size=32, epochs=10, verbose=1)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open(MODEL_FILENAME, 'wb') as f:
    f.write(tflite_model)
