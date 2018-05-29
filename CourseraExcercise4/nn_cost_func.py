# Import the necessary pachages
import scipy.io
import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt

# Sigmoid function
def sigmoid(value):
	return 1.0 / (1.0 + np.exp(-value))

# Regularized cost function
def reg_cost(theta, arr_x, arr_y, lambda1):	
	
	theta1 = np.reshape(theta[0:25 * 401], (25, 401))
	theta2 = np.reshape(theta[25 * 401: len(theta)], (10, 26))

	h, nan = feedforward(theta1, theta2, x_vals)

	first_half = np.multiply(arr_y, np.log(h))
	second_half = np.multiply((1 - arr_y), np.log(1 - h))

	cost1 = np.sum((-1.0 / m) * (first_half + second_half))
	cost2 = (lambda1 / (2.0 * m)) * (np.sum(theta1 ** 2) - np.sum(theta1[:,0] ** 2))
	cost3 = (lambda1 / (2.0 * m)) * (np.sum(theta2 ** 2) - np.sum(theta2[:,0] ** 2))
	cost = cost1 + cost2 + cost3
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

# Sigmoid function gradient
def sigmoid_gradient(value):
	h = sigmoid(value)
	return h * (1 - h)

# Backpropagation
def backprop(theta, arr_x, arr_y_train, lambda1):
	# Change our theta values back into their original shape
	theta_rand1 = np.reshape(theta[0:25 * 401], (25, 401))
	theta_rand2 = np.reshape(theta[25 * 401: len(theta)], (10, 26))

	a3, a2 = feedforward(theta_rand1, theta_rand2, arr_x)
	Delta2 = 0
	Delta1 = 0

	for i in range(500): #FIXME
		delta3 = a3[i] - arr_y_train[i]                   # Vector length 10
		delta3 = np.reshape(delta3, (len(delta3), 1))     # (10, 1) matrix
		temp_a2 = np.reshape(a2[i], (len(a2[i]), 1))      # (26, 1) matrix
		delta2 = np.multiply(np.dot(theta_rand2.T, delta3), temp_a2 * (1 - temp_a2))

		Delta2 = Delta2 + np.dot(delta3, temp_a2.T)       # (10, 26) matrix
		temp_arr_x = np.reshape(arr_x[i], (len(arr_x[i]), 1))
		# We need to remove delta2[0] from Delta1
		Delta1 = Delta1 + np.delete(np.dot(delta2, temp_arr_x.T), 0, axis = 0) # (25, 401) matrix
		

	# Compute the unregularized gradient
	D1_temp = (1.0 / m) * Delta1 
	D2_temp = (1.0 / m) * Delta2

	# Compute the regularized gradient
	D1 = (1.0 / m) * Delta1 + (lambda1 / m) * theta_rand1
	D1[0:, 0:1] = D1_temp[0:, 0:1]    # (25, 401) matrix
	D2 = (1.0 / m) * Delta2 + (lambda1 / m) * theta_rand2
	D2[0:, 0:1] = D2_temp[0:, 0:1]    # (10, 26) matrix

	D1 = np.ravel(D1)
	D2 = np.ravel(D2)
	D_vals = np.concatenate((D1, D2), axis = 1)

	return D_vals

####### Neural Network #######

# Extract the provided data. We need to use scipy since the data is in a matlab file format
data = scipy.io.loadmat('ex4data1.mat')
data_thetas = scipy.io.loadmat('ex4weights.mat')

'''
The x array is under the name 'X', the y array is under the name 'y'
x_vals ia a (5000, 400) array and y_vals is a (5000, 1) array
'''
x_vals = data['X']
y_vals = data['y']

'''
The array for theta1 is under the name 'Theta1' and the array for theta2 is under the name 'Theta2'
theta1_vals is a (25, 401) array and theta2_vals is a (10, 26) array

'''
theta1_vals = data_thetas['Theta1'] # FIXME
theta2_vals = data_thetas['Theta2'] # FIXME

#Set what lambda value we want to use
lambda1 = 1

# Add a column of ones to our array of x_vals
m = len(x_vals)    # Number of training examples (rows)
arr_ones = np.ones((m, 1))
x_vals = np.hstack((arr_ones, x_vals))        # (5000, 401) matrix

# Set up an array that will be either 1 or 0 depending on which number we are looking at
y_vals_train = np.zeros((len(y_vals), 10))

for i in range(10):
	# Set up an array with the values that stand for each number (10 stands for 0)
	arr_num = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	
	for j in range(len(y_vals)):
		if (y_vals[j] == arr_num[i]):
			y_vals_train[j, i:] = 1
		
		else:
			y_vals_train[j, i:] = 0

'''
#For testing cost and feedforward
hypothesis, nan = feedforward(theta1_vals, theta2_vals, x_vals)
J_val = reg_cost(hypothesis, x_vals, y_vals_train, theta1_vals, theta2_vals, lambda1)
print J_val
#J_val = 10.5
#This differs from the value in the intruction sheet
'''

####### Backpropagation ########

# Randomly initialize our theta values in a range [-0.12, 0.12]
n = len(x_vals[0])   # Number of columns
random_theta1 = np.random.rand(25, n)                        # (25, 401) matrix
random_theta1 = random_theta1 * 2 * 0.12 - 0.12

random_theta2 = np.random.rand(10, len(random_theta1) + 1)   # (10, 26) matrix
random_theta2 = random_theta2 * 2 * 0.12 - 0.12

# Combine these into a 1-dimension vector
random_theta1_1D = np.ravel(random_theta1)   # 10025 1-D vector
random_theta2_1D = np.ravel(random_theta2)   # 260 1_D vector
theta_vals = np.concatenate((random_theta1_1D, random_theta2_1D), axis = 1)
print theta_vals.shape
print random_theta1_1D.shape
print random_theta2_1D.shape

grad = backprop(theta_vals, x_vals, y_vals_train, lambda1)

print scipy.optimize.check_grad(reg_cost, backprop, theta_vals, x_vals, y_vals_train, lambda1)

'''	
	# Use scipys minimize function to compute the theta values
	minimum = scipy.optimize.minimize(fun = reg_cost, x0 = theta_vals, method = 'BFGS', jac = reg_cost_gradient, args = (x_vals, y_vals_train, lambda_all[k]))#, options = {'disp': True}
	
	# Create a new array that consists of all of the new theta values
	theta_new = np.reshape(minimum.x, (1, len(minimum.x)))
	prob = sigmoid(theta_new, x_vals)
	prob = np.reshape(prob, (len(prob), 1))
	
	if (i == 0):
		prob_all = prob
	else:
		prob_all = np.hstack((prob_all, prob))	

	print "Iteration: %g" %(i + 1)

# Find the largest value in each column
best_prob = np.zeros((len(prob_all), 1))
for i in range (len(prob_all)):
	best_prob[i, 0] = np.argmax(prob_all[i, :])
	 
# Find how accurate our program was with identifying the correct number
correct_guess = np.zeros((10, 1))
for i in range(len(best_prob)):
	if (best_prob[i] == y_vals[i]):
		correct_guess[y_vals[i]] = correct_guess[y_vals[i]] + 1
	
	if (best_prob[i] == 0 and y_vals[i] == 10):
		correct_guess[0] = correct_guess[0] + 1
	
# Calculate the percentage
correct_guess = (correct_guess / 500) * 100

# Check the results
print correct_guess

correct_guesses[k] = correct_guess
'''

