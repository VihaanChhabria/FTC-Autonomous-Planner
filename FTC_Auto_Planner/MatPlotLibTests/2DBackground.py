# importing required modules
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

img = plt.imread(r"C:\Users\vihaa\Python-Examples\FTC_Auto_Planner\MatPlotLibTests\background.jpg")

def mouse_move(event):
    xdata, ydata = event.xdata, event.ydata

    if not (xdata == None):
        
        #print(f"x: {x2}, y: {y2}")
        #xdata = 1
        #ydata = 1
        
        x = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
        y = []

        slope = ydata/xdata

        for xNumber in x:
            yNumber = xNumber*slope
            if (yNumber > 10) or (yNumber < -10):
                print("in")
                return
            y.append(yNumber)

        print(x)
        print(y)


        plt1.plot(x, y, color ='r')
        print("hi")
        plt.draw()

    

# setting a style to use
plt.style.use('fivethirtyeight')

# define subplots and their positions in figure
fig, plt1 = plt.subplots(layout='constrained')

# plotting points on each subplot

#x, y = create_plot('linear')

plt.connect('motion_notify_event', mouse_move)
plt1.imshow(img, extent=[-10, 10, -10, 10])
#plt1.plot(x, y, color ='r')
plt1.set_title('$y_1 = x$')

# function to show the plot
plt.show()
