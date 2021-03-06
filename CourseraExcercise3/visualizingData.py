# Import the necessary pachages
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import random

# Extract the provided data. We need to use scipy since the data is in a matlab file format
data = scipy.io.loadmat('ex3data1.mat')

# The x array is under the name 'X', the y array is under the name 'y'
x_vals = data['X']
y_vals = data['y']

# Set up a an array of random 10 images [a (10, 400) vector]
random_images = np.random.randint(0, x_vals.shape[0] - 1, 10)
images = x_vals[random_images]


# Now reshape images back into (20, 20) matrices and transpose to flip images right-side up
image = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
image2 = image

for i in range(len(random_images)):
	temp = np.reshape(images[i], (20, 20))
	temp = np.transpose(temp)
	image[i] = temp

# Put all the images together
total_images = np.concatenate(image, axis = 1)

# Plot the results
plt.imshow(total_images, cmap = 'binary')
plt.show()

# Plotting 0 to 9
for i in range (len(image2)):
	temp = np.reshape(x_vals[i * 500], (20, 20))
	temp = temp.T
	image2[i] = temp

# Put all the images together
total_images2 = np.concatenate(image2, axis = 1)

# Plot the results
plt.imshow(total_images2, cmap = 'binary')
plt.show()


