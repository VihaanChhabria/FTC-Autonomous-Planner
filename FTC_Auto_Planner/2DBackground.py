# importing required modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import Button

img = plt.imread(r"C:\Users\vihaa\FTC-Autonomous-Planner\FTC_Auto_Planner\MatPlotLibTests\background.jpg")

x_left_vals = []
y_left_vals = []

x_right_vals = []
y_right_vals = []

startposition = False
endposition = False

def on_click(event):
    global startposition
    global endposition

    xdata, ydata = event.xdata, event.ydata
    buttonpressed = event.button

    if not (xdata == None):
        if (startposition and (buttonpressed == MouseButton.LEFT)):
            x_left_vals.append(xdata)
            y_left_vals.append(ydata)
            startposition = False
        elif (endposition and (buttonpressed == MouseButton.LEFT)):
            x_right_vals.append(xdata)
            y_right_vals.append(ydata)
            endposition = False

        # clear the plot and redraw the points
        plt.clf()
        plt.scatter(x_left_vals, y_left_vals, color ='lime', marker='x', s = 130)
        plt.scatter(x_right_vals, y_right_vals, color ='lime', marker='*', s = 130)
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.imshow(img, extent=[-10, 10, -10, 10])        

        axstart = fig.add_axes([0.9, 0.05, 0.1, 0.075])
        bstart = Button(axstart, 'Start')
        bstart.on_clicked(start_button)

        axend = fig.add_axes([0.9, 0.2, 0.1, 0.075])
        bend = Button(axend, 'End')
        bend.on_clicked(end_button)

        plt.draw()

        #startposition = False
        #endposition = False
    
def start_button(event):
    global startposition
    startposition = True

def end_button(event):
    global endposition
    endposition = True

# setting a style to use
plt.style.use('fivethirtyeight')

# define subplots and their positions in figure
fig, ax = plt.subplots()

"""axstart = fig.add_axes([0.9, 0.05, 0.1, 0.075])
bstart = Button(axstart, 'Start')
bstart.on_clicked(start_button)

axend = fig.add_axes([0.9, 0.2, 0.1, 0.075])
bend = Button(axend, 'End')
bend.on_clicked(end_button)"""

plt.connect('button_press_event', on_click)

ax.imshow(img, extent=[-10, 10, -10, 10])
#plt1.plot(x, y, color ='r')
ax.set_title('$y_1 = x$')

# function to show the plot
plt.show()
