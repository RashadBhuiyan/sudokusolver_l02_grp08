import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Sequential, layers
from keras.datasets import mnist

## remove zeros from mnist dataset since sudoku has no 0
def removeZero(x_arr, y_arr):
    indices = (y_arr > 0).nonzero()
    return x_arr[indices], y_arr[indices]

## preprocess image for model fitting
def preProcessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img/255
    return img

## based on model by https://github.com/shubham99bisht/Handwritten-digit-recognition-MNIST
def createModel():

    model = Sequential()
    model.add(layers.Conv2D(filters=64, kernel_size = (3,3), activation="relu", input_shape=(28,28,1)))
    model.add(layers.Conv2D(filters=64, kernel_size = (3,3), activation="relu"))

    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(filters=128, kernel_size = (3,3), activation="relu"))
    model.add(layers.Conv2D(filters=128, kernel_size = (3,3), activation="relu"))

    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.BatchNormalization())    
    model.add(layers.Conv2D(filters=256, kernel_size = (3,3), activation="relu"))
        
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
        
    model.add(layers.Flatten())
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(512,activation="relu"))
        
    model.add(layers.Dense(10,activation="softmax"))
        

    # model = Sequential()
    # model.add(layers.Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
    # model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    # model.add(layers.Dropout(0.2))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(128, activation='relu'))
    # model.add(layers.Dense(10, activation='softmax'))

    # model = Sequential()
    # model.add((layers.Conv2D(60, (5,5), input_shape = (28, 28, 1), activation = "relu")))
    # model.add((layers.Conv2D(60, (5,5), activation = "relu")))
    # model.add(layers.MaxPooling2D(pool_size = (2,2)))
    # model.add((layers.Conv2D(30, (3,3), activation = "relu")))
    # model.add((layers.Conv2D(30, (3,3), activation = "relu")))
    # model.add(layers.MaxPooling2D(pool_size = (2,2)))
    # model.add(layers.Dropout(0.5))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(500, activation='relu'))
    # model.add(layers.Dropout(0.5))
    # model.add(layers.Dense(10, activation='softmax'))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

# initializes the handwriting (MNIST) dataset
(mnist_x_train, mnist_y_train), (mnist_x_test, mnist_y_test) = mnist.load_data()

mnist_x_train, mnist_y_train = removeZero(mnist_x_train, mnist_y_train)
mnist_x_test, mnist_y_test = removeZero(mnist_x_test, mnist_y_test)

mnist_x_train = mnist_x_train.reshape((mnist_x_train.shape[0], 28, 28, 1)).astype('float32')
mnist_x_test = mnist_x_test.reshape((mnist_x_test.shape[0], 28, 28, 1)).astype('float32')

mnist_x_train /= 255
mnist_x_test /= 255


images = []
classes = []
# initializes the printed number dataset
for i in range(10):
    path = "dataset/" + str(i)
    imageFiles = os.listdir(path)
    for file in imageFiles:
        curImg = cv2.imread(path + '/' + file)
        images.append(curImg)
        classes.append(i)

images = np.array(images)
classes = np.array(classes)

# portion off data as training / test sets
x_train, x_test, y_train, y_test = train_test_split(images, classes, test_size=0.2)
x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=0.2)

x_train = np.array(list(map(preProcessing, x_train)))
x_test = np.array(list(map(preProcessing, x_test)))
x_validation = np.array(list(map(preProcessing, x_validation)))

# reshape printed digit dataset to fit mnist
x_train = x_train.reshape(len(x_train), 28, 28, 1)
x_test = x_test.reshape(len(x_test), 28, 28, 1)
x_validation = x_validation.reshape(len(x_validation), 28, 28, 1)

# duplicate printed data for augmented dataset using ImageDataGenerator
x_train = x_train.repeat(50, axis=0)
y_train = y_train.repeat(50)

# duplicate MNIST data for augmented dataset using ImageDataGenerator
mnist_x_train = mnist_x_train.repeat(20, axis=0)
mnist_y_train = mnist_y_train.repeat(20)

# combine MNIST and printed datasets
x_train = np.concatenate((x_train, mnist_x_train), axis=0)
x_test = np.concatenate((x_test, mnist_x_test), axis=0)

y_train = np.concatenate((y_train, mnist_y_train), axis=0)
y_test = np.concatenate((y_test, mnist_y_test), axis=0)

x_train, y_train = shuffle(x_train, y_train)

# create augmented data generator
dataGen = ImageDataGenerator(width_shift_range = 0.1, 
                            height_shift_range = 0.1,
                            zoom_range=0.2,
                            shear_range=0.1,
                            rotation_range=10
                            )
dataGen.fit(x_train)

# create category matrix for y classification
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
y_validation = to_categorical(y_validation, 10)

model = createModel()
print (model.summary())

batch = 50
epoch = 10
stepsPerEpoc = 10000

# fit model
history = model.fit(dataGen.flow(x_train, y_train, batch_size=batch), steps_per_epoch = stepsPerEpoc, epochs = epoch, validation_data = (x_validation, y_validation), shuffle = 1)

model.save("printed_new.h5")

score = model.evaluate(x_test, y_test)
print('Score: ', score[0])
print('Accuracy: ', score[1])