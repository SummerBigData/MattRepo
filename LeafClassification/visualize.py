# Import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg           	 	 # Reading images to numpy arrays
from sklearn.metrics.pairwise import cosine_similarity

####### Definitions #######
def visualize_leaves(images, y, classes, show1, show2):
	'''
	Create a grid of random leaves and/or display all the images of a specified leaf species
	Displaying the specifed species works for displaying guesses of the test set too

	Parameters:
	images - list of images of the leaves
	y - list of numbers ranging from 0-98 where each number represents a species of leaf
	classes - list of the names of the species
	show1 - shows the grid of leaves if true
	show2 - shows the images of a specified species of leaves if true	
	'''

	# For displaying a grid of random leaves
	if show1:
		# Setting up our grid
		num_row = 15
		num_col = 15

		# Setting up each row
		for i in range(num_row):
			# Setting up each image in said row
			for j in range(num_col):
				if (j == 0):
					images1 = images[j + i * num_col,:,:,0]
		
				else:
					temp = images[j + i * num_col,:,:,0]
					images1 = np.concatenate((images1, temp), axis = 1)
			
			# Attach new row below previous one	
			if (i == 0):
				images2 = images1
			else:
				images2 = np.concatenate((images2, images1), axis = 0)

		# Displaying the grid
		a = plt.figure(1)
		plt.imshow(images2, cmap = 'binary', interpolation = 'none')
		a.show()

	# For displaying images of a specified leaf species (Works for guessed leaves in test set)
	if show2:
		
		# Give a list of the id associated with each species
		for i in range(len(classes)):
			print i, classes[i]
		
		# Ask for what species to display	 
		species = input('What leaf species would you like to look at? ')
		print 'You chose', classes[species]

		# Find how many images of that species there is
		hold = []
		num_img = 0

		# Create a list holding each index that image is in
		for i in range(len(y)):
			if y[i] == species:
				num_img += 1
				hold.append(i)

		# Check if we have an odd amount of images (relevant for displaying the test leaves after predictions)
		if num_img % 2 != 0:
			print 'Number of images is not even!'
			# Print the odd image separately
			c = plt.figure(1)
			plt.imshow(images[hold[num_img - 1],:,:,0], cmap = 'binary', interpolation = 'none')
			ax = plt.gca()
			ax.axes.get_xaxis().set_visible(False)
			ax.axes.get_yaxis().set_visible(False)
			c.show()
			num_img -= 1	
		
		# Display the images in 2 rows
		count = 0
		for j in range(len(y)):
			if y[j] == species:
				count += 1
				# First row
				if count < (num_img / 2) + 1:
					if (count == 1):
						pics = images[j,:,:,0]
		
					else:
						temp = images[j,:,:,0]
						pics = np.concatenate((pics, temp), axis = 1)
				# Second row
				elif count > (num_img / 2) and count < num_img + 1:
					if (count == (num_img / 2) + 1):
						pics2 = images[j,:,:,0]
	
					else:
						temp = images[j,:,:,0]
						pics2 = np.concatenate((pics2, temp), axis = 1)
	
		# Display the images
		al = np.concatenate((pics, pics2), axis = 0)

		b = plt.figure(num_img)
		plt.imshow(al, cmap = 'binary', interpolation = 'none')
		ax = plt.gca()
		ax.axes.get_xaxis().set_visible(False)
		ax.axes.get_yaxis().set_visible(False)
		b.show()

	# Show multiple images at once if need be
	if show1 or show2:
		raw_input()
	return

# Checking how similar each image is to one another of the same leaf species
def image_similarity(train, y, classes):
	'''
	See how similar each image is to one another of the same leaf species
	
	Parameters:
	train - list of images in the training set
	y - list of numbers ranging from 0-98 where each number represents a species of leaf
	classes - list of the names of the species
	'''
	
	# Cycle through each class
	for i in range(len(classes)):
		# Find all of the image of said class
		temp = np.where(y == i)

		# Stick all of the images in a list
		temp1 = []
		for j in range(len(temp[0])):
			temp1.append(train[temp[0][j],:,:,0])

		# Use the first image of the list to compare to the remaining 9
		summ = 0	
		for k in range(len(temp1) - 1):
			summ += np.asscalar(cosine_similarity(temp1[0].reshape(1,-1), temp1[k + 1].reshape(1,-1)))

		# Print the average cosine similarity for each species
		print classes[i], 'cosine similarity:', summ / (len(temp1) - 1)

	return

def plt_perf(name, f1, f2, p_loss=False, p_acc=False, val=False, size=(15,9), save=False):
	'''
	From https://www.kaggle.com/limitpointinf0/leaf-classifier-knn-nn?scriptVersionId=3352828
	Plot the model stats for the keras model (accuracy, loss)
	
	Parameters:
	name - model used
	f1 - filename to save loss plot to
	f2 - filename to save accuracy plot to
	p_loss - tells if we want to display the loss plot
	p_acc - tells if we want ot display the accuracy plot
	val- tells if we want to show the stats of our validation set
	size - size of our plots
	save - tells if we want to save our plots or not
	'''

	if p_loss or p_acc:
		# Display loss plot
		if p_loss:
			plt.figure(figsize = size)
			plt.title('Loss')
			plt.plot(name.history['loss'], 'b', label='loss')
			if val:
				plt.plot(name.history['val_loss'], 'r', label='val_loss')
			plt.xlabel('Epochs')
			plt.ylabel('Value')
			plt.legend()
			# plt.show()
			if save:
				print 'Saving loss...'
				plt.savefig(f1)

		# Display accuracy plot
		if p_acc:
			plt.figure(figsize = size)
			plt.title('Accuracy')
			plt.plot(name.history['acc'], 'b', label='acc')
			if val:
 				plt.plot(name.history['val_acc'], 'r', label='val_acc')
			plt.xlabel('Epochs')
 			plt.ylabel('Value')
			plt.legend()
 			# plt.show()
			if save:
				print 'Saving accuracy...'
 				plt.savefig(f2)
	else:
		print 'No plotting since all parameters set to false.'

	return

def confusion(y_pred, y, classes, test_ids, num_classes):

	# Find the leaves that have lower probabilities 
	x = []
	x_val = []
	y_val = []
	total = 0
	threshold = 0.99
	for i in range(len(y_pred)):
		if (np.amax(y_pred[i]) < threshold):
			# Index where the highest probability is
			x = np.append(x, np.argmax(y_pred[i]))
			# ID of the leaf we are looking at
			x_val = np.append(x_val, test_ids[i])
			# Where the leaf is in the matrix (what row)
			y_val = np.append(y_val, i)
			# Tally up the total number of leaves
			total += 1
	print 'Total number of <', threshold, ' predictions: %g' %(total)

	# Set up an array that ranges from 0 - 98 to set up the class numbers
	x2 = np.ones(num_classes)
	for i in range(len(x2)):
		x2[i] = i

	most_conf = np.zeros(len(x2))
	# Cycle through each leaf that had a low probability
	for i in range(len(x)):
		# Cycle through each class number
		for j in range(len(x2)):
			# Display the leaves with the lower probabilities
			if (x2[j] == x[i]):
				# Find what the guess was
				print 'Species guessed:', classes[j]
				# Find the id of the corresponding image
				print 'ID associated with leaf:', int(x_val[i])
				
				# Get top 3 predictions
				most_conf = np.zeros(len(x2))
    				top3_ind = y_pred[int(y_val[i])].argsort()[-5:]
    				top3_species = np.array(classes)[top3_ind]
    				top3_preds = y_pred[int(y_val[i])][top3_ind]
				most_conf[top3_ind] += 1 

    				# Display the top 3 predictions and the actual species
    				print("Top 5 Predicitons:")
    				for k in range(4, -1, -1):
        				print "\t%s (%s): %s" % (top3_species[k], top3_ind[k], top3_preds[k])

				# Display the image of the leaf
				string1 = 'data_provided/unzip_images/images/' + str(int(x_val[i])) + '.jpg'
				img = mpimg.imread(string1)
				string2 = 'Species guessed: ' + classes[j] + ', ID: ' + str(int(x_val[i]))
				plt.title(string2)
				ax = plt.gca()
				ax.axes.get_xaxis().set_visible(False)
				ax.axes.get_yaxis().set_visible(False)
				plt.imshow(img, cmap = 'binary')
				plt.show()

				# Display the probabilities for that leaf
				plt.bar(x2, y_pred[int(y_val[i])])
				plt.title('Probability of Each Class for ID: ' + str(int(x_val[i])))
				plt.xlabel('Class Number')
				plt.ylabel('Probability')
				plt.show()

				print '\n'
	print most_conf	
	return
