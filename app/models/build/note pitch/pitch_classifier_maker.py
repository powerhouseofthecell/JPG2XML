from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from modelBuilder import buildModel
import datetime

# build the model that we will use
model = buildModel()

# define the input image size
ts = (150, 150)

# I'm going to augment my extremely limited dataset so as to enhance the number of images that my algorithm is exposed to
# as much as possible
# rescale is a value that will be multiplied across the input data to rescale it. in this case, it makes every input
# a ratio or proportion to 255
# shear_range gives a number for performing transformations that move each pixel by an amount that is related to shear force
# zoom_range tells the computer how much to zoom in on or out of the pictures
# and horizontal_flip just tells the computer to flip some of the images
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=.2, zoom_range=.2, horizontal_flip=True)

# our validation data will only be rescaled, no other transformations
test_datagen = ImageDataGenerator(rescale=1./255)

# now we have to prepare the data for use
# it has been stored into two directories underneath a directory labeled data
train_generator = train_datagen.flow_from_directory('data/train', target_size=ts, batch_size = 161, class_mode='categorical')
validation_generator = test_datagen.flow_from_directory('data/validation', target_size=ts, batch_size=5, class_mode='categorical')

# and now we fit the model to the data
model.fit_generator(train_generator, samples_per_epoch=6440, nb_epoch=25, validation_data=validation_generator, nb_val_samples=55)

# find the current date and time
dt = datetime.datetime.now()

# save the model, for use later in classifying notes
model.save('./app/models/pitch/pitch_model-%s-%s-%s-%s-%s.h5' % (dt.minute, dt.hour, dt.day, dt.month, dt.year))
