from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

def buildModel():
    # initialize the kind of model we'll be building
    model = Sequential()
    
    # add the first convolutional/maxpooling layer duo***THE SHAPE MAY NEED TO CHANGE, NBD, JUST NOTE***
    model.add(Convolution2D(16, 3, 3, input_shape=(3, 150, 150)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # next layer is also a convolution/maxpooling layer duo
    model.add(Convolution2D(128, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(5, 5)))

    # next layer is also a convolution/maxpooling layer duo
    model.add(Convolution2D(16, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # final convolutional layer duo for the model
    model.add(Convolution2D(64, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # the model now will output a 3D feature map with height, width, and various aspects

    # I now need to convert the output from that layer into a "1D" vector
    model.add(Flatten())

    # and here are more layers with some dropout to reduce the model's
    # accidentally learning patterns that are irrelevant
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(.6))
    model.add(Dense(64))
    model.add(Activation('tanh'))
    model.add(Dropout(.4))
    model.add(Dense(11))
    model.add(Activation('softmax'))

    # and finally, compile and return the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

