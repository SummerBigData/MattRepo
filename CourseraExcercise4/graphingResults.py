import numpy as np
import matplotlib.pyplot as plt

# Set up the data
train500 = [93.5, 96.7, 84.2, 82.4, 85.3, 70.7, 88.7, 88.6, 76.2, 78.2]
train500 = np.reshape(train500, (len(train500), 1))
train5000 = [97.6, 98.2, 90.5, 90.2, 95, 88.1, 94.2, 92.3, 89.1, 90.7]
train5000 = np.reshape(train5000, (len(train5000), 1))
train10000 = [98.1, 98.1, 93, 93, 95.3, 89.6, 95.1, 93.6, 92.9, 91.1]
train10000 = np.reshape(train10000, (len(train10000), 1))
train20000 = [97.3, 98.3, 94.6, 93.1, 96, 92.5, 96.5, 94.2, 93.3, 92.8]
train20000 = np.reshape(train20000, (len(train20000), 1))
train40000 = [98.4, 98.3, 94.5, 95, 95.9, 93.2, 96, 95.2, 92.8, 93.5]
train40000 = np.reshape(train40000, (len(train40000), 1))
train60000 = [97.9, 98.8, 94.5, 95.4, 95.8, 93.9, 96.5, 94.4, 94.5, 93.6]
train60000 = np.reshape(train60000, (len(train60000), 1))

# For printing out the results in a bar graph
x = [0, 1, 2 ,3 ,4 ,5 ,6 ,7 , 8 ,9]
x = np.reshape(x, (len(x), 1))
fig1 = plt.figure()
ax = plt.subplot(111)
ax.bar(x - 0.35, train500, width = 0.14, align = 'center', color = 'goldenrod')
ax.bar(x - 0.21, train5000, width = 0.14, align = 'center', color = 'blue')
ax.bar(x - 0.07, train10000, width = 0.14, align = 'center', color = 'green')
ax.bar(x + 0.07, train20000, width = 0.14, align = 'center', color = 'black')
ax.bar(x + 0.21, train40000, width = 0.14, align = 'center', color = 'purple') 
ax.bar(x + 0.35, train60000, width = 0.14, align = 'center', color = 'firebrick')
plt.title("Accuracy with different training sizes")
plt.xlim(left = -0.5, right = 9.5)
plt.ylim(70)
plt.xlabel("Number")
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
plt.ylabel("Percentage of correct guesses")
ax.legend([500, 5000, 10000, 20000, 40000, 60000], loc = 'upper right', ncol = 6, prop = {'size': 9})
plt.show()

# Plot the average correct guesses for all 6 cases
x2 = [1, 2, 3, 4, 5, 6]
averages = [84.45, 92.69, 93.98, 94.86, 95.28, 95.53]
fig2 = plt.figure()
plt.bar(x2, averages, align = 'center', color = 'red')
plt.title('Average Accuracy for Different Training Sizes')
plt.ylim(80)
plt.xlabel('Training size')
plt.xticks(x2, [500, 5000, 10000, 20000, 40000, 60000])
plt.ylabel('Average accuracy')
plt.show()
