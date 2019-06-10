#######################################################################################
# There is currently no clean way to call the populate_db() and train_model() functions
# but from the Django shell. As these tasks only need to be done once, that's not such
# a problem.
#
# In a future version, they might be integrated into a password-protected view
#######################################################################################

import keras
import os
import numpy as np
from .models import Digit


def classify_image(arr):
    """
    Takes a 2D NumPy array and runs it through a classifier. Returns the resulting category.
    :param arr: 2D NumPy array
    :return:
    """
    model = keras.models.load_model(os.path.join("digit_painter", "static", "mnist_trained_model.h5"))
    arr = arr[np.newaxis, ..., np.newaxis]
    pred = model.predict(arr)
    return pred.argmax(), pred.max()


def populate_db():
    """
    Populates the Django database with the MNIST data.

    NOTE: This deletes all MNIST entries in the database, so they will never be duplicated
    :return:
    """
    # Load mnist data
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Delete existing MNIST entries
    Digit.objects.filter(entry_type="MNIST_train").delete()
    Digit.objects.filter(entry_type="MNIST_test").delete()

    # Save arrays
    for ii in range(len(x_train)):
        d = Digit(
            base64_data=Digit.serialize(x_train[ii]),
            category=str(y_train[ii]),
            entry_type="MNIST_train")
        d.save()

    for ii in range(len(x_test)):
        d = Digit(
            base64_data=Digit.serialize(x_test[ii]),
            category=str(y_test[ii]),
            entry_type="MNIST_test")
        d.save()

    return None


def train_model():
    """
    Trains a model based on the data in the Django database
    :return:
    """

    # Load digits from the database and extract data. Labels have to be transformed to categorical one-hot vectors
    x_train, y_train = zip(*[
        (entry.get_array(), entry.category) for entry in
        Digit.objects.filter(entry_type__endswith="train")])
    x_train = np.array(x_train)
    y_train = keras.utils.to_categorical(np.array(y_train))

    x_test, y_test = zip(*[
        (entry.get_array(), entry.category) for entry in
        Digit.objects.filter(entry_type__endswith="test")])
    x_test = np.array(x_test)
    y_test = keras.utils.to_categorical(np.array(y_test))

    # Transform input to be 4D
    x_train = x_train[..., None]
    x_test = x_test[..., None]

    # create model
    model = keras.models.Sequential()

    # add model layers
    model.add(keras.layers.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        input_shape=x_train.shape[1:]))
    model.add(keras.layers.MaxPool2D())
    model.add(keras.layers.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        kernel_initializer="glorot_uniform"))
    model.add(keras.layers.MaxPool2D())
    model.add(keras.layers.Conv2D(
        filters=32, kernel_size=3, activation='relu',
        kernel_initializer="glorot_uniform"))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(
        units=10, activation='softmax',
        kernel_initializer="glorot_uniform"))

    # compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=5)
    model.save(os.path.join("digit_painter", "static", "mnist_trained_model.h5"))
