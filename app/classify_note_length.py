from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Model, load_model
import numpy as np
from PIL import Image
import os, os.path
from config import length_model, targetSize

# this function should be called when the images have been created and assigned to the tmp/data directory
# *** please also go back and zero index the notes, just to make this whole thing a little bit easier ***
def classifyLength():
    # load the model that we will be using to classify the image
    # maybe pass in the name of the model to use as an argument?
    # or potentially include a default and use that unless you train your own?
    model = load_model(length_model)

    # data to be classified will need to be rescaled
    prediction_datagen = ImageDataGenerator(rescale=1./255)

    # count how many files are being classified
    numOfImages = len([name for name in os.listdir('./app/tmp/data/.') if os.path.isfile('./app/tmp/data/' + name)])

    # pull all the data to be classified from the tmp directory
    prediction_generator = prediction_datagen.flow_from_directory('./app/tmp', target_size=targetSize, batch_size=1, class_mode=None, shuffle=False)

    # classify the data
    results = model.predict_generator(prediction_generator, numOfImages)

    return(results.round())
