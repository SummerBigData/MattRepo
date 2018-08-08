# Import the necessary packages
import numpy as np				 	 # Allow for easier use of arrays and linear algebra
import data_setup                                        # Python code for setting up the data
import visualize					 # Python code for visualizing images
import pandas as pd                         	 	 # For reading in and writing files
import image_rotation
from sklearn.linear_model import LogisticRegression      # sklearn's log reg
from sklearn.preprocessing import StandardScaler 	 # Preprocessing
from sklearn.model_selection import GridSearchCV         # Helps find the best parameters for our model

####### Global variables #######
global_num_prob = 2
global_max_dim = 50
global_num_classes = 99
filename = 'sklearn_log_reg.csv'
threshold = 0.95

seed = 2
np.random.seed(seed)

####### Code #######
# Set up the data given to us
train_list, test_list, train_ids, test_ids, train, test, y, y_train, classes = data_setup.data()

# We need to reshape our images so they are all the same dimensions
train_mod_list = data_setup.reshape_img(train_list, global_max_dim)
test_mod_list = data_setup.reshape_img(test_list, global_max_dim)

# train_mod_list, y_train, train, train_list, y = image_rotation.augment()

# Grab more features to train on
train, test = data_setup.engineered_features(train, test, train_list, test_list)

# Grab even more features with openCV
train, test = data_setup.more_features(train, test, train_list, test_list)

# Let's apply PCA to the images and attach them to the pre-extracted features
train, test = data_setup.apply_PCA(train, test, train_mod_list, test_mod_list, global_max_dim, y, classes)

# fit calculates the mean and transform centers and scales the data so we have 0 mean and unit variance
scaler = StandardScaler().fit(train)
x_train = scaler.transform(train)
x_test = scaler.transform(test)

# Run multiple times to obtain an average of probabilities
probabilities = []

# We will use the solver 'lbfgs'
log_reg = LogisticRegression(solver = 'lbfgs', verbose = 1, max_iter = 500, multi_class = 'multinomial')

# Find the best parameters for our model
gsCV = GridSearchCV(log_reg, param_grid = {'C': [100000.0, 10000.0, 1000.0],
						'tol': [0.0001, 0.00001, 0.000001]},
						scoring = 'neg_log_loss', refit = True,
						verbose = 1, n_jobs = -1, cv = 5)

# FIT IT
gsCV.fit(x_train, y)

# Print the score from each run
print('best params: ' + str(gsCV.best_params_))
for params, mean_score, scores in gsCV.grid_scores_:
 	print '%0.3f (+/-%0.03f) for %r' % (mean_score, scores.std(), params)
	print scores

# Predict for One Observation (image)
y_pred = gsCV.predict_proba(x_test)

'''
rand_forest = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            	max_depth=2, max_features='auto', max_leaf_nodes=None,
            	min_impurity_decrease=0.0, min_impurity_split=None,
            	min_samples_leaf=1, min_samples_split=2,
            	min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
            	oob_score=False, random_state=0, verbose=1, warm_start=False)

rand_forest.fit(x_train, y)
y_pred = rand_forest.predit(x_test)
'''

# Save our numpy array to a .npy file for later use
np.save('probabilities/sklearn' + str(seed), y_pred)


# visualize.confusion(y_pred, y, classes, test_ids, global_num_classes, train_mod_list, theshold)

# Set up the predictions into the correct format to submit to Kaggle
y_pred = pd.DataFrame(y_pred, index = test_ids, columns = classes)

# Save predictions to a csv file to submit
print 'Saving to file', filename, '...'
fp = open(filename,'w')
fp.write(y_pred.to_csv())

print 'Finished.'

