# Import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import data_setup
from scipy.ndimage import rotate
from keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics.pairwise import cosine_similarity   # Used for checking how similar images are to one another

global_max_dim = 50

seed = 2
np.random.seed(seed)

def augment():
	# Set up the data given to us
	train_list, test_list, train_ids, test_ids, train, test, y, y_train, classes = data_setup.data()

	# We need to reshape our images so they are all the same dimensions
	train_mod_list = data_setup.reshape_img(train_list, global_max_dim)
	test_mod_list = data_setup.reshape_img(test_list, global_max_dim)

	# Let's create more images for us
	datagen = ImageDataGenerator(rotation_range=20, zoom_range=0.2, fill_mode='nearest')

	datagen.fit(train_mod_list)

	# Configure batch size and retrieve one batch of images
	temp = []
	temp2 = []
	temp3 = []
	temp4 = []
	temp5 = []
	for i in range(len(train_mod_list)):
		j = 0
		temp.append(train_mod_list[i].reshape(global_max_dim, global_max_dim))
		temp2.append(y_train[i])
		temp3.append(train[i:i + 1])
		temp4.append(train_list[i])
		temp5.append(y[i])		
		

		for X_batch, y_batch in datagen.flow(train_mod_list[i:i + 1], y_train[i:i + 1], batch_size=9):
			temp.append(X_batch.reshape(global_max_dim, global_max_dim))
			temp2.append(y_batch)
			temp3.append(train[i:i + 1])
			temp4.append(train_list[i])
			temp5.append(y[i])
		
			j += 1
			if j == 9:
				break
	
	temp_arr = np.zeros((len(temp), global_max_dim, global_max_dim))
	temp2_arr = np.zeros((len(temp2), 99))
	temp3_arr = np.zeros((len(temp3), 192))
	temp5_arr = np.zeros(len(temp5))
	print temp5_arr.shape

	for i in range(len(temp)):
		temp_arr[i] = temp[i]
		temp2_arr[i] = temp2[i]
		temp3_arr[i] = temp3[i]
		temp5_arr[i] = temp5[i]

	train_mod_list = temp_arr.reshape(len(temp_arr), global_max_dim, global_max_dim, 1)
	y_train = temp2_arr
	train = temp3_arr
	train_list = temp4
	y = temp5_arr

	return train_mod_list, y_train, train, train_list, y

