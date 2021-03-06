# Import the necessary packages
import numpy as np
import scipy.signal as ss

####### Definitions #######
# Sigmoid function
def sigmoid(value):
	return 1.0 / (1.0 + np.exp(-value))

def convolve(patch_dim, num_features, images, W, b, ZCA_white, mean_patch):
	'''
	Parameters:
	patch_dim - dimension of patch region (8)
	num_features - amount of features we are using (400)
	images - matrix of our images (m, 64, 64, 3)
	W - our matrix of our weights (400, 192)
	b - our bias term (400, 1)
	ZCA_white - The whitening matrix we computed earlier (192, 192)
	mean_patch - the mean of our patches that we computed earlier (1, 192)

	Returns:
	convolved_features - matrix of convolved features (400, m, 57, 57)
	'''
	# Number of images
	m = images.shape[0]
	# Dimension of image
	img_dim = images.shape[1]
	# Number of channels
	num_channel = images.shape[3]
	
	convolved_features = np.zeros((num_features, m, img_dim - patch_dim + 1, img_dim - patch_dim + 1)) # (400, m , 57, 57)

	# Precompute the matrices that will be used during the convolution
	# We need to compute WT, where W is our weights and T is our whitening matrix, and (b-WTx_bar)
	WT = np.dot(W, ZCA_white)                  # (400, 192)

	# Reformat WT into a (400, 8, 8, 3) matrix
	s = patch_dim ** 2
	WT_reform = np.zeros((len(WT), patch_dim, patch_dim, num_channel))
	for i in range(len(WT)):
		### IMPORTANT ###
		# Make sure the colors are reshaped correctly ([0:64] for first color, [64:128] for second, [128:192] for third)
    		WT_reform[i,:,:,0] = WT[i, :s].reshape(patch_dim, patch_dim)
   		WT_reform[i,:,:,1] = WT[i, s:2*s].reshape(patch_dim, patch_dim)
    		WT_reform[i,:,:,2] = WT[i, 2*s:].reshape(patch_dim, patch_dim)

	b_mean = b - np.dot(WT, mean_patch.T)         # (400, 1)

	# For each image
	for i in range(m):
		# For each feature
		for j in range(num_features):
		
			# Convolution of image with feature matrix for each channel
			convolved_image = np.zeros((img_dim - patch_dim + 1, img_dim - patch_dim + 1))   # (57, 57)
			
			# For each color
			for k in range(num_channel):
				# Obtain the feature (patch_dim, patch_dim) needed during the convolution
				feature = np.zeros((patch_dim, patch_dim))                               # (8, 8)
				feature = WT_reform[j, :, :, k]
	
				# Flip the feature matrix because of the definition of convolution
				feature = np.flipud(np.fliplr(np.squeeze(feature)))
	
				# Obtain the image
				im = np.squeeze(images[i, :, :, k])                                                # (64, 64)
	
				# Convolve feature with im, add the result to convolved_image
				convolved_image += ss.convolve2d(im, feature, mode = 'valid', boundary = 'fill', fillvalue = 0)	# (57, 57)

			# Add our bias term
			convolved_image += b_mean[j, 0]

			# Apply the sigmoid function to get the hidden activation
			# The convolved feature is the sum of the convolved values for all channels
			convolved_features[j, i, :, :] = sigmoid(convolved_image)

	return convolved_features
			

