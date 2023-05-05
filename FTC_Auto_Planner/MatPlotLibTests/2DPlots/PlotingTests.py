import matplotlib.pyplot as plt

class LineDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.xs = []
        self.ys = []
        self.line = None
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes != self.ax:
            return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        if len(self.xs) == 2:
            self.ax.plot(self.xs, self.ys)
            self.xs = []
            self.ys = []
            self.fig.canvas.draw()

if __name__ == '__main__':
    ld = LineDrawer()
    plt.show()
