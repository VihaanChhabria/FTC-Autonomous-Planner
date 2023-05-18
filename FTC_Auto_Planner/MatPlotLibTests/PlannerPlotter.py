import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from matplotlib.backend_bases import MouseButton

fig, ax = plt.subplots()
img = plt.imread(r"C:\Users\vihaa\FTC-Autonomous-Planner\FTC_Auto_Planner\MatPlotLibTests\background.jpg")
ax.imshow(img, extent=[-10, 10, -10, 10])

class Main:
    x_left_vals = []
    y_left_vals = []

    x_right_vals = []
    y_right_vals = []

    def onclick(self, event):
        print("in")
        xdata, ydata = event.xdata, event.ydata
        buttonpressed = event.button
        print(buttonpressed)
        print(event)
        if not (xdata == None):
            if (buttonpressed == MouseButton.LEFT):
                self.x_left_vals.append(xdata)
                self.y_left_vals.append(ydata)
            elif (buttonpressed == MouseButton.RIGHT):
                self.x_right_vals.append(xdata)
                self.y_right_vals.append(ydata)

            plt.scatter(self.x_left_vals, self.y_left_vals, color ='lime', marker='x', s = 130)
            plt.scatter(self.x_right_vals, self.y_right_vals, color ='lime', marker='*', s = 130)

            fig.canvas.draw()
callback = Main()

plt.connect('button_press_event',callback.onclick)

plt.show()