from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Model, load_model
import numpy as np
from PIL import Image
import os, os.path

# this function should be called when the images have been created and assigned to the tmp/data directory
# *** please also go back and zero index the notes, just to make this whole thing a little bit easier ***
def classify():
    # load the model that we will be using to classify the image
    # maybe pass in the name of the model to use as an argument?
    # or potentially include a default and use that unless you train your own?
    model = load_model('model96.h5')

    # data to be classified will need to be rescaled
    prediction_datagen = ImageDataGenerator(rescale=1./255)

    # count how many files are being classified
    numOfImages = len([name for name in os.listdir('tmp/data/.') if os.path.isfile('tmp/data/' + name)])

    # pull all the data to be classified from the tmp directory
    prediction_generator = prediction_datagen.flow_from_directory('tmp', target_size=(150, 150), batch_size=1, class_mode=None, shuffle=False)

    # classify the data
    results = model.predict_generator(prediction_generator, numOfImages)

    return(results.round())

# print the results ***FOR NOW: THIS SHOULD BECOME OBSOLETE SHORTLY
print(classify())

#########
# KEEP IN MIND, THIS REQUIRES THAT A TMP DIRECTORY BE CREATED WITH SUBDIRECTORY DATA IN ORDER FOR THIS TO WORK
# ALSO, THE RESULTS COULD EASILY BE RETURNED IN SUCH A WAY AS TO BE READABLE
# THE INDICES OF THE RESULTS ARRAY CORRESPOND TO THE 'POSITION' OF THE NOTE IN THE MUSICAL PIECE
#########
