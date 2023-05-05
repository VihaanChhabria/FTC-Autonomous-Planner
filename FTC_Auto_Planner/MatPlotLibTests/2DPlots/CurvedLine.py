# importing the required modules
import matplotlib.pyplot as plt
import numpy as np

# setting the x - coordinates
x = np.arange(0, 360, 10)
# setting the corresponding y - coordinates
y = np.sin(np.radians(x))

# plotting the points
plt.plot(x, y)

# function to show the plot
plt.show()
