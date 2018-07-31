# Import the necessary packages
# Misc
import numpy as np				 	 # Allow for easier use of arrays and linear algebra
import matplotlib                                	 # Imported for use of matplotlib.use('Agg')
# matplotlib.use('Agg')                            	 # Use if submitting job to the supercomputer
import pandas as pd                         	 	 # For reading in and writing files
import scipy.ndimage as ndi            	   	 	 # Finding the center of the leaves
import argparse                                  	 # For inputing values outside of the code
import visualize                                 	 # Python code for visualizing images
import data_setup                                        # Python code for seting up the data

# sklearn
from sklearn.preprocessing import StandardScaler 	 # Preprocessing

# Keras
from keras.models import Sequential, Model      	 # Linearly sets up model, allows the use of keras' API
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, Activation, concatenate, Input
from keras.utils import plot_model            		 # Visualizing model
from keras.callbacks import EarlyStopping 	         # Used to prevent overfitting
from keras.callbacks import ModelCheckpoint              # Gives us the best weights obtained during fitting
from keras.preprocessing.image import ImageDataGenerator, NumpyArrayIterator, array_to_img
from keras.optimizers import SGD                         # Enable the modification of optimizer SGD


####### Global Variables #######
parser = argparse.ArgumentParser()
parser.add_argument('disp_stats', 
	help = 'Use 1/0 (True/False) to indicate if you want to display model stats or not.', type = int)
parser.add_argument('save_stats', 
	help = 'Use 1/0 (True/False) to indicate if you want to save model stats or not.', type = int)
parser.add_argument('save_prob', 
	help = 'Use 1/0 (True/False) to indicate if you want to save probabilities or not.', type = int)
parser.add_argument('leaf_stats', 
	help = 'Use 1/0 (True/False) to indicate if you want to display leaf images and stats or not.', type = int)
parser.add_argument('global_max_epochs', help = 'Max amount of epochs allowed.', type = int)
parser.add_argument('global_batch_size', help = 'Number of samples per gradient update.', type = int)

args = parser.parse_args()

global_num_train = 990
global_num_test = 594
global_hidden_layers = [500, 250] #[500, 250]
global_output_layer = 99
global_num_classes = 99
global_max_dim = 50

filename1 = 'graphs/lossEpoch' + str(args.global_max_epochs) + 'Batch' + str(args.global_batch_size) + 'Softmax.png'
filename2 = 'graphs/accEpoch' + str(args.global_max_epochs) + 'Batch' + str(args.global_batch_size) + 'Softmax.png'
filename3 = 'submissions/submissionEpoch' + str(args.global_max_epochs) + 'Batch' + str(args.global_batch_size) + 'Softmax.csv'
model_file = 'bestWeights2.hdf5'

# Set up a seed so that our results don't fluctuate over multiple tests
np.random.seed(1)

####### Definitions #######
def create_model_softmax():
	'''
	This model uses only the pre-extracted features of the leaves to create a softmax regression model
	Returns the built model
	'''
		
	mod1 = Sequential()	
	
	mod1.add(Dense(global_hidden_layers[0], input_dim = input_layer, activation = 'relu'))
	mod1.add(Dropout(0.3))
	
	# For loop allows for easier adding and removing of hidden layers adjusting their sizes
	if (len(global_hidden_layers) > 1):
		for i in range(len(global_hidden_layers) - 1):
			mod1.add(Dense(global_hidden_layers[i + 1], activation = 'relu'))
			mod1.add(Dropout(0.2))	
	
	mod1.add(Dense(global_output_layer, activation = 'softmax'))
	
	return mod1

def extra_layers(first):

	x2 = Flatten()(first)
	x2 = Dense(1000, activation = 'relu')(x2)
	x2 = Dropout(0.2)(x2)
	x2 = Dense(800, activation = 'relu')(x2)
	x2 = Dropout(0.2)(x2)
	x2 = Dense(600, activation = 'relu')(x2)
	x2 = Dropout(0.2)(x2)

	return  x2

def create_model_combined():
	'''
	This model uses both the images and the and pre-extracted features of the leaves to create a CNN model
	Returns the built model
	'''
	# Obtaining features from the images
	first_input = Input(shape=(global_max_dim, global_max_dim, 1))
	x = Conv2D(filters = 16, kernel_size = (5, 5), activation ='relu', padding = 'Same')(first_input)
	x = MaxPool2D(pool_size = (2, 2))(x)
	x = Dropout(0.2)(x)
	x = Conv2D(filters = 32, kernel_size = (5, 5), activation ='relu', padding = 'Same')(x)
	x = MaxPool2D(pool_size = (2, 2))(x)
	x = Dropout(0.2)(x)
	x = Flatten()(x)
	x = Dense(192, activation = 'relu')(x)
	final_first_input_layer = Dropout(0.2)(x)

	'''
	# Merging convolved features with nn features of images
	x2 = extra_layers(first_input)
	merge_prequel = concatenate([final_first_input_layer, x2])
	
	x = Dense(200, activation = 'relu')(merge_prequel)
	'''	

	# Merging features from images with pre-extracted features
	second_input = Input(shape=(input_layer, ))
	merge_one = concatenate([final_first_input_layer, second_input])

	x = Dense(global_hidden_layers[0], activation = 'relu')(merge_one)
	x = Dropout(0.2)(x)
	
	# For loop allows for easier adding and removing of hidden layers adjusting their sizes
	if (len(global_hidden_layers) > 1):
		for i in range(len(global_hidden_layers) - 1):
			x = Dense(global_hidden_layers[i + 1], activation = 'relu')(x)
			x = Dropout(0.2)(x)
	
	final = Dense(global_output_layer, activation = 'softmax')(x)
	model = Model(inputs=([first_input, second_input]), outputs=final)

	return model

def combined_generator(imgen, X):
    '''
    A generator to train our keras neural network. It
    takes the image augmenter generator and the array
    of the pre-extracted features.
    It yields a minibatch and will run indefinitely
    '''
    while True:
        for i in range(X.shape[0]):
            # Get the image batch and labels
            batch_img, batch_y = next(imgen)
            # This is where that change to the source code we
            # made will come in handy. We can now access the indicies
            # of the images that imgen gave us.
            x = X[i]
            yield [batch_img, x], batch_y

def augment_fit(mod, f1, t_list, x, y):
	'''
	Fitting our model that uses both augmented images and pre-extracted features 
	(Only applicable for the combined model)

	Parameters:
	mod - model used
	f1 - file name the best model is saved under
	t_list - list of modified training images
	x - matrix of training pre-extracted features
	y - matrix of testing pre-extracted features

	Returns the stats of the model
	'''

	print 'Using the augmented data fit_generator.'

	'''
	Since fit_generator does not support validation_split we must create our 
	own validation data first (10% of data)
	'''
	t_val = t_list[global_num_train - 99: global_num_train]
	x_val = x[global_num_train - 99: global_num_train]
	y_val = y[global_num_train - 99: global_num_train]
	
	# We need to remove the validation data from our test set
	t_train = t_list[0: global_num_train - 99]
	x_train = x[0: global_num_train - 99]
	y_train = y[0 : global_num_train - 99]

	# Creating our augmented data
	# ImageDataGenerator generates batches of tensor image data with real-time data augmentation.
	datagen = ImageDataGenerator(rotation_range=20,
    		zoom_range=0.2,
   		horizontal_flip=True,
   		vertical_flip=True,
   		fill_mode='nearest')

	# Flow takes data & label arrays, generates batches of augmented data.
	x_batch = datagen.flow(t_train, y_train, batch_size = args.global_batch_size)	

	early_stopper= EarlyStopping(monitor = 'val_loss', patience = 280, verbose = 1, mode = 'auto')
	model_checkpoint = ModelCheckpoint(f1, monitor = 'val_loss', verbose = 1, save_best_only = True)

	spe = int(len(t_train) / args.global_batch_size)
	# fit_generator fits the model on batches with real-time data augmentation
	history = mod.fit_generator(combined_generator(x_batch, x_train), steps_per_epoch = spe,
		epochs = args.global_max_epochs, verbose = 0, validation_data = ([t_val, x_val], y_val),
		callbacks = [early_stopper, model_checkpoint])
	
	return history

def nn_fit(mod, f1, x, y):
	'''
	Fitting our model that uses only the pre-extracted features (Only applicable for the neural network model)

	Parameters:
	mod - model used
	f1 - file name the best model is saved under
	x - matrix of training pre-extracted features
	y - matrix of testing pre-extracted features

	Returns the stats of the model
	'''

	print 'Using the neural network fit.'
	early_stopper= EarlyStopping(monitor = 'val_loss', patience =300, verbose = 1, mode = 'auto')
	model_checkpoint = ModelCheckpoint(f1, monitor = 'val_loss', verbose = 1, save_best_only = True)

	history = mod.fit(x, y, epochs = args.global_max_epochs, batch_size = args.global_batch_size,
		verbose = 0, validation_split = 0.1, shuffle = True, 
		callbacks = [early_stopper, model_checkpoint])	

	return history

def combined_fit(mod, f1, t_list, x, y):
	'''
	Fitting our model that uses both image and pre-extracted features (Only applicable for the combined model)

	Parameters:
	mod - model used
	f1 - file name the best model is saved under
	t_list - list of modified training images
	x - matrix of training pre-extracted features
	y - matrix of testing pre-extracted features

	Returns the stats of the model
	'''

	print 'Using the combined network fit.'
	early_stopper= EarlyStopping(monitor = 'val_loss', patience = 300, verbose = 1, mode = 'auto')
	model_checkpoint = ModelCheckpoint(model_file, monitor = 'val_loss', verbose = 1, save_best_only = True)

	history = mod.fit(([t_list, x]), y, epochs = args.global_max_epochs,
		batch_size = args.global_batch_size, verbose = 0, validation_split = 0.1, shuffle = True,
		callbacks = [early_stopper, model_checkpoint])	

	return history	

####### Code #######
# Set up the data given to us
train_list, test_list, train_ids, test_ids, train, test, y, y_train, classes = data_setup.data()

# Grab more features to train on
train, test = data_setup.engineered_features(train, test, train_list, test_list)

# We need to reshape our images so they are all the same dimensions
train_mod_list = data_setup.reshape_img(train_list, global_max_dim)
test_mod_list = data_setup.reshape_img(test_list, global_max_dim)

# train, test = data_setup.more_features(train, test, train_list, test_list)

# Let's apply PCA to the images and attach them to the pre-extracted features
train, test = data_setup.apply_PCA(train, test, train_mod_list, test_mod_list, global_max_dim)



'''
# fit_transform() calculates the mean and std and also centers and scales data
x_train = StandardScaler().fit_transform(train)
x_test = StandardScaler().fit_transform(test)
'''
# fit calculates the mean and transform centers and scales the data so we have 0 mean and unit variance
scaler = StandardScaler().fit(train)
x_train = scaler.transform(train)
x_test = scaler.transform(test)

# Look at images and some stats of leaves
if args.leaf_stats:
	print 'Displaying images...'
	visualize.image_similarity(train_mod_list, y, classes)
	visualize.visualize_leaves(train_mod_list, y, classes, show1 = False, show2 = True)
	print 'Finished.'

# Set up our input layer size
input_layer = x_train.shape[1]

# Setting up the Keras neural network
# Choose a model
model = create_model_softmax()
# model = create_model_combined()

# Compile our model
sgd = SGD(lr=0.01, momentum=0.9, decay=1e-6, nesterov=False)
model.compile(optimizer = sgd, loss = 'categorical_crossentropy', metrics = ['accuracy'])
print model.summary()
# plot_model(model, to_file = 'modelSoftmax2.png', show_shapes = True)

'''
Choose a fit for our model
Early stopping helps prevent over fitting by stopping our fitting function 
if our val_loss doesn't decrease after a certain number of epochs (called patience)
Model checkpoint saves the best weights obtained during training
'''

# history = augment_fit(model, model_file, train_mod_list, x_train, y_train)
history = nn_fit(model, model_file, x_train, y_train)
# history = combined_fit(model, model_file, train_mod_list, x_train, y_train)

# Check Keras' statistics
if args.disp_stats:
	print 'Displaying stats...'
	visualize.plt_perf(history, filename1, filename2, p_loss = True, p_acc = True, val = True,
		save = args.save_stats)
	print 'Finished.'

# Reload our best weights
model.load_weights(model_file)

# Test our model on the test set
y_pred = model.predict(x_test)
print '\n'

# Let's see what leaves our network struggled the most with
# visualize.confusion(y_pred, y, classes, test_ids, global_num_classes, train_mod_list)

# Set up the predictions into the correct format to submit to Kaggle
y_pred = pd.DataFrame(y_pred, index = test_ids, columns = classes)

# Save predictions to a csv file to submit
if args.save_prob:
	print 'Saving to file', filename3, '...'
	fp = open(filename3,'w')
	fp.write(y_pred.to_csv())

print 'Finished.'

