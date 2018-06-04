# Import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import random

####### Definitions #######
# Sigmoid function
def sigmoid(value):
	return 1.0 / (1.0 + np.exp(-value))

# Regularized cost function
def reg_cost(theta, arr_x, arr_y):	
	# Reshape our thetas back into their original shape  
	arr_theta1 = np.reshape(theta[0:25 * n], (25, n))
	arr_theta2 = np.reshape(theta[25 * n: len(theta)], (10, 26))

	# Find our hypothesis
	h, nano = feedforward(arr_theta1, arr_theta2, arr_x)

	# Find the average activation of each hidden unit averaged over the training set
	rho_hat = (1.0 / m) * 

	# Calculate the cost
	first_third = np.multiply(arr_y, np.log(h))
	second_third = np.multiply((1.0 - arr_y), np.log(1.0 - h))
	third_third = global_beta * (global_rho * log(global_rho / rho_hat) + (1 - global_rho) * log((1 - global_rho) / (1 - rho_hat)))

	cost1 = np.sum((-1.0 / m) * (first_half + second_half))
	cost2 = (lambda1 / (2.0 * m)) * (np.sum(arr_theta1 ** 2) - np.sum(arr_theta1[:,0] ** 2))
	cost3 = (lambda1 / (2.0 * m)) * (np.sum(arr_theta2 ** 2) - np.sum(arr_theta2[:,0] ** 2))
	cost = cost1 + cost2 + cost3 + third_third
	'''
	# Incase we get booted early
	if (global_iterations % 20 == 0):
		print cost
		np.savetxt(file_name, theta, delimiter = ',')
	'''
	return cost

# Feedforward
def feedforward(theta1, theta2, arr_x):

	# We will be running our sigmoid function twice
	a2 = sigmoid(np.dot(arr_x, theta1.T))	

	# Add a column of ones to our array of a2
	arr_ones = np.ones((m, 1))
	a2 = np.hstack((arr_ones, a2))        # (5000, 26) matrix

	# Second run
	a3 = sigmoid(np.dot(a2, theta2.T))    # (5000, 10) matrix

	return a3, a2

# Backpropagation
def backprop(theta, arr_x, arr_y_train):
	# Change our theta values back into their original shape
	arr_theta1 = np.reshape(theta[0:global_hidden_size * n], (global_hidden_size, n))
	arr_theta2 = np.reshape(theta[global_hidden_size * n: len(theta)], (10, 26))

	a3, a2 = feedforward(arr_theta1, arr_theta2, arr_x)
	Delta2 = 0
	Delta1 = 0

	# Find the average activation of each hidden unit averaged over the training set
	rho_hat = (1.0 / m) * 	

	for i in range(len(arr_x)):
		delta3 = a3[i] - arr_y_train[i]                   # Vector length 10
		
		delta3 = np.reshape(delta3, (len(delta3), 1))     # (10, 1) matrix
		temp_a2 = np.reshape(a2[i], (len(a2[i]), 1))      # (26, 1) matrix
		# Add in sparsity parameter
		KL_divergence = global_beta * (-(global_rho / rho_hat) + (1 - global_rho) / (1 - rho_hat)
		delta2 = np.multiply((np.dot(arr_theta2.T, delta3) + KL_divergence), temp_a2 * (1 - temp_a2))

		Delta2 = Delta2 + np.dot(delta3, temp_a2.T)       # (10, 26) matrix
		temp_arr_x = np.reshape(arr_x[i], (len(arr_x[i]), 1))
		
		# We need to remove delta2[0] from Delta1
		Delta1 = Delta1 + np.delete(np.dot(delta2, temp_arr_x.T), 0, axis = 0) # (25, 401) matrix
		
	# Compute the unregularized gradient
	D1_temp = (1.0 / m) * Delta1 
	D2_temp = (1.0 / m) * Delta2
	
	# Compute the regularized gradient
	D1 = (1.0 / m) * Delta1 + (global_lambda1 / float(m)) * arr_theta1
	D1[0:, 0:1] = D1_temp[0:, 0:1]    # (25, 401) matrix
	D2 = (1.0 / m) * Delta2 + (global_lambda1 / float(m)) * arr_theta2
	D2[0:, 0:1] = D2_temp[0:, 0:1]    # (10, 26) matrix

	# Changed the gradient into a one dimensional vector
	D1 = np.ravel(D1)
	D2 = np.ravel(D2)
	D_vals = np.concatenate((D1, D2))

	return D_vals

####### Generate training set #######

# Extract the provided data. We need to use scipy since the data is in a matlab file format
images_data = scipy.io.loadmat('starter/IMAGES.mat')

# The images that we need to extract are under the name 'IMAGES'
images = images_data['IMAGES']
print images.shape

patch_size = 8       # We want to use 8x8 patches
num_patches = 10000  # Total number of patches we will have

# Set up an array of zeros for the patches (64, 10000)
patches = np.zeros((patch_size ** 2, num_patches))

# Let's look at one of the images
pick_image = 0
pick_image = int(input('Enter digit representing an image (0-9):'))
while (pick_image > 9 or pick_image < 0):
	pick_image = int(input('Please pick a digit in the range 0-9:'))

image = images[:,:, pick_image]
plt.imshow(image, cmap = 'binary')
# plt.show()

# Now we want to break the image up into patches
for i in range(len(patches[0])):
	int_random = random.randint(0, 504)
	temp = image[int_random: int_random + 8, int_random: int_random + 8]
	temp = np.reshape(temp, (64, 1))
	patches[:, i:i+1] = temp

# Check to make sure our code is running correctly
image2 = np.reshape(patches[:,0:1], (8, 8))
plt.imshow(image2, cmap = 'binary', interpolation = 'none')
# plt.show()

####### Sparse autoencoder objective #######
global_visible_size = 64
global_hidden_size = 25
global_lambda1 = 1
global_beta = 3
global_rho = 1              # Sparsity parameter

# We need to add a row of ones onto patches


# Initialize parameters randomly based on layer sizes.
r  = sqrt(6) / sqrt(hiddenSize+visibleSize+1);   # We'll choose weights uniformly from the interval [-r, r]
random_theta1 = np.random.rand(global_hidden_size, global_visible_size)      # (25, 64) matrix
random_theta1 = random_theta1 * 2 * r - r
random_theta2 = np.random.rand(global_visible_size + 1, global_hidden_size)      # (65, 25) matrix      
random_theta2 = random_theta2 * 2 * r - r

# Combine these into a 1-dimension vector
random_theta1_1D = np.ravel(random_theta1)   
random_theta2_1D = np.ravel(random_theta2)   
theta_vals = np.concatenate((random_theta1_1D, random_theta2_1D), axis = 1)

# Gradient checking from scipy to see if our backprop function is working properly. Theta_vals needs to be a 1-D vector.
# print scipy.optimize.check_grad(reg_cost, backprop, theta_vals, x_vals, y_vals_train)
# Recieved a value of N/A
