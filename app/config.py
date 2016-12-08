# this line sets which model the code will use when classifying the data
# the default is what we found to be the most accurate
# this string is the path from the directory where config sits to the model
# (the .h5 file)
length_model = './app/models/length/length_model99.h5'

# similarly, this line sets the model for classifying each image's pitch
pitch_model = './app/models/pitch/pitch_model99_2.h5'

# this line establishes where to pull the templates from
templates = ['./app/templates/t1.jpg', './app/templates/t2.jpg']

# define the target size of the images
targetSize = (150, 150)
