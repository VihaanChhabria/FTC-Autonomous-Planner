import matplotlib.pyplot as plt

# initialize empty lists to store the x and y coordinates of the points
x_vals = []
y_vals = []

def onclick(event):
    # add the clicked point to the lists
    x_vals.append(event.xdata)
    y_vals.append(event.ydata)
    # clear the plot and redraw the points
    plt.clf()
    plt.scatter(x_vals, y_vals)

    plt.xlim(0, 10)
    plt.ylim(0, 10)
    
    plt.draw()

# create the initial plot with no points
fig, ax = plt.subplots()
plt.xlim(0, 10)
plt.ylim(0, 10)

# register the onclick event handler
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# show the plot
plt.show()
