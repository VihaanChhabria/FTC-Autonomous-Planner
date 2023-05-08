import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from matplotlib.backend_bases import MouseButton

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.3)

axcolor = 'lightgoldenrodyellow'
rax = fig.add_axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('Start', 'End'))

class Main:
    startposition = False
    endposition = False

    x_left_vals = []
    y_left_vals = []

    x_right_vals = []
    y_right_vals = []

    def radiofunc(self, label):
        radiodict = {'Start': self.startposition, 'End': self.endposition}
        typeposition = radiodict[label]

        if typeposition == self.startposition:
            self.startposition = True
            self.endposition = False
        else:
            self.startposition = False
            self.endposition = True

    def onclick(self, event):
        print("in")
        xdata, ydata = event.xdata, event.ydata
        buttonpressed = event.button
        if not (xdata == None):
            if (self.startposition and (buttonpressed == MouseButton.LEFT)):
                self.x_left_vals.append(xdata)
                self.y_left_vals.append(ydata)
            elif (self.endposition and (buttonpressed == MouseButton.RIGHT)):
                self.x_right_vals.append(xdata)
                self.y_right_vals.append(ydata)

            plt.scatter(self.x_left_vals, self.y_left_vals, color ='lime', marker='x', s = 130)
            plt.scatter(self.x_right_vals, self.y_right_vals, color ='lime', marker='*', s = 130)

            fig.canvas.draw()
callback = Main()
radio.on_clicked(callback.radiofunc)
plt.connect('button_press_event',callback.onclick)

plt.show()