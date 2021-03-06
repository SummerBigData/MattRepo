# Import the necessary packages
import struct as st
import gzip
import numpy as np
import scipy.optimize
import scipy.io
import cnn_convolve, cnn_pooling
import random
import sys

####### Global variables #######
global_num_images = 60000   # Max of 60000
global_image_dim = 28
global_patch_dim = 15
global_visible_size = global_patch_dim ** 2
globel_output_size = global_visible_size
global_hidden_size = 100
global_pool_dim = 2

####### Definitions #######
# Sigmoid function
def sigmoid(value):
	return 1.0 / (1.0 + np.exp(-value))

# Reading in MNIST data files
def read_idx(filename, n=None):
	with gzip.open(filename) as f:
		zero, dtype, dims = st.unpack('>HBB', f.read(4))
		shape = tuple(st.unpack('>I', f.read(4))[0] for d in range(dims))
		arr = np.fromstring(f.read(), dtype=np.uint8).reshape(shape)
		if not n is None:
			arr = arr[:n]
		return arr

# Checking the convolution code
def check_conv(im, conv_feat, W1, b1):
	m = len(im)
	for i in range(1000):
		# Pick a random data patch
		feature_num = np.random.randint(0, global_hidden_size - 1)
		image_num = np.random.randint(0, m)
		image_row = np.random.randint(0, global_image_dim - global_patch_dim)
		image_col = np.random.randint(0, global_image_dim - global_patch_dim)
	
		patch = im[image_num, image_row: image_row + global_patch_dim, image_col: image_col + global_patch_dim]
		patch = patch.reshape(1, global_patch_dim ** 2)
		
		features = sigmoid(np.dot(patch, W1.T) + np.tile(np.ravel(b1), (m, 1)))
		
		if (abs(features[0, feature_num] - conv_feat[feature_num, image_num, image_row, image_col]) > 1e-9):
			print 'Convolved feature does not match activation from autoencoder'
			print 'Feature Number    : ', feature_num
			print 'Image Number      : ', image_num
			print 'Image Row         : ', image_row
			print 'Image Column      : ', image_col
			print 'Convolved feature : ', conv_feat[feature_num, image_num, image_row, image_col]
			print 'Sparse AE feature : ', features[1, feature_num]
			print 'Error: Convolved feature does not match activation from autoencoder'
			sys.exit()
		
	print 'Congratz! Your convolution code passed the test.'

	return	

# Checking the pooling code
def check_pool():
	# Set up a test matrix to test on
	test_matrix = np.arange(1, 65).reshape(8, 8)

	# Manually compute our results to check against
	expected_matrix = np.array((np.mean(np.mean(test_matrix[0:4, 0:4])), np.mean(np.mean(test_matrix[0:4, 4:8])),
		np.mean(np.mean(test_matrix[4:8, 0:4])), np.mean(np.mean(test_matrix[4:8, 4:8])))).reshape(2, 2)

	test_matrix = np.reshape(test_matrix, (1, 1, 8, 8))

	pool_feat = np.squeeze(cnn_pooling.pooling(4, test_matrix))

	if np.any(np.not_equal(pool_feat, expected_matrix) == True):
		print 'Pooling incorrect'
		print 'Expected'
		print expected_matrix
		print 'Got'
		print pool_feat
		sys.exit()
	else:
		print 'Congratz! Your pooling code passed the test.'

	return

# Change our weights and bias terms back into their proper shapes
def reshape(theta):
	W1 = np.reshape(theta[0:global_hidden_size * global_visible_size], (global_hidden_size, global_visible_size))
	W2 = np.reshape(theta[global_hidden_size * global_visible_size: 2 * global_hidden_size * global_visible_size],
		(global_visible_size, global_hidden_size))
	b1 =np.reshape(theta[2 * global_hidden_size * global_visible_size: 2 * global_hidden_size * global_visible_size + global_hidden_size],
		(global_hidden_size, 1))
	b2 =np.reshape(theta[2 * global_hidden_size * global_visible_size + global_hidden_size: len(theta)], (global_visible_size, 1))
	
	return W1, W2, b1, b2

# Extract the MNIST training data sets
def get_train(size):
	x_vals = read_idx('provided_data/train-images-idx3-ubyte.gz', size)
	x_vals = x_vals / 255.0
	x_vals = np.reshape(x_vals, (x_vals.shape[0], (x_vals.shape[1] * x_vals.shape[2])))
	y_vals = read_idx('provided_data/train-labels-idx1-ubyte.gz', size)
	y_vals = np.reshape(y_vals, (len(y_vals), 1))
	print x_vals.shape, y_vals.shape
	
	return x_vals, y_vals

# Extract the MNIST testing data sets
def get_test(size):
	x_vals = read_idx('provided_data/t10k-images-idx3-ubyte.gz', size)
	x_vals = x_vals / 255.0
	x_vals = np.reshape(x_vals, (x_vals.shape[0], (x_vals.shape[1] * x_vals.shape[2])))
	y_vals = read_idx('provided_data/t10k-labels-idx1-ubyte.gz', size)
	y_vals = np.reshape(y_vals, (len(y_vals), 1))
	print x_vals.shape, y_vals.shape
	
	return x_vals, y_vals

####### Code #######
# Import the weights we need
final_theta = np.genfromtxt('outputs/HL100/finalWeightsMNISTSize10000Patches15x15L0.0001B0.5Rho0.01HL100.out')

# We need to reshape our final_theta values and only use W1 and b1
W1_final, W2_final, b1_final, b2_final = reshape(final_theta)

# Extract the MNIST training data sets
train_images, __ = get_train(global_num_images)
num_train_images = len(train_images)

# Reshape our images so that they are (num_train_images , 28, 28)
train_images = np.reshape(train_images, (len(train_images), len(train_images[0]) / global_image_dim, len(train_images[0]) / global_image_dim))

'''
# FOR TESTING OUR CONVOLUTION AND POOLING CODE
# Grab a small amount of images to test our convolve code on
train_test_images = train_images[0:8, :]

# Implement convolution
convolved_features = cnn_convolve.convolve(global_patch_dim, global_hidden_size,
	train_test_images, W1_final, b1_final)

# We will now check our convolution
check_conv(train_test_images, convolved_features, W1_final, b1_final)

# Implement pooling
pooled_features = cnn_pooling.pooling(global_pool_dim, convolved_features)

# Now we need to test if our pooling is correct
check_pool()
'''
# Extract the MNIST testing data sets
test_images, __ = get_test(global_num_images)
num_test_images = len(test_images)

# Reshape our images so that they are (num_test_images , 28, 28)
test_images = np.reshape(test_images, (len(test_images), len(test_images[0]) / global_image_dim, len(test_images[0]) / global_image_dim))

# Now to start running the full data set
# We need to run our convolution and pooling 20 features at a time so we don't run out of memory
step_size = 20
assert global_hidden_size % step_size == 0, 'Step size should divide hidden size'

pooled_features_train = np.zeros((global_hidden_size, num_train_images,
	np.floor((global_image_dim - global_patch_dim + 1) / global_pool_dim),
	np.floor((global_image_dim - global_patch_dim + 1) / global_pool_dim)))

pooled_features_test = np.zeros((global_hidden_size, num_test_images,
	np.floor((global_image_dim - global_patch_dim + 1) / global_pool_dim),
	np.floor((global_image_dim - global_patch_dim + 1) / global_pool_dim)))

for i in range(global_hidden_size / step_size):
	feature_start = i * step_size 
	feature_end = (i + 1) * step_size

	print 'Step %g: features %g to %g' %(i + 1, feature_start + 1, feature_end)
	Wt = W1_final[feature_start: feature_end, :]
	bt = b1_final[feature_start: feature_end, :]

	print 'Convolving and pooling train images.'
	convolved_features = cnn_convolve.convolve(global_patch_dim, step_size,
		train_images, Wt, bt)
	pooled_features = cnn_pooling.pooling(global_pool_dim, convolved_features)
	pooled_features_train[feature_start: feature_end, :, :, :] = pooled_features

	print 'Convolving and pooling test images.'
	convolved_features = cnn_convolve.convolve(global_patch_dim, step_size,
		test_images, Wt, bt)
	pooled_features = cnn_pooling.pooling(global_pool_dim, convolved_features)
	pooled_features_test[feature_start: feature_end, :, :, :] = pooled_features



# Save our data for later	
np.savetxt('outputs/convPoolTrainFeaturesSize60000StepSize50V2.out', np.ravel(pooled_features_train))
np.savetxt('outputs/convPoolTestFeaturesSize10000StepSize50V2.out', np.ravel(pooled_features_test))

