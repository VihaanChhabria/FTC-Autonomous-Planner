import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image

class Plotter:
    def __init__(self):
        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.points = []
        self.line, = self.ax.plot([], [], color='blue')

    def plot_data(self, event):
        # Get the coordinates of the clicked point
        x = event.xdata
        y = event.ydata

        if x is not None and y is not None:
            # Get the current marker
            marker = self.marker_var.get()

            # Plot the clicked point with the current marker and the same color
            self.ax.plot(x, y, marker=marker, color='lime')
            self.points.append((x, y, marker))

            self.plot_line()

            self.canvas.draw()

    def plot_line(self):
        if len(self.points) > 1:
            # Extract x and y coordinates from the points
            self.x_values = [point[0] for point in self.points]
            self.y_values = [point[1] for point in self.points]

            if self.line:
                # If the line object exists, update its data
                self.line.set_data(self.x_values, self.y_values)
            else:
                # If the line object doesn't exist, create a new line plot
                self.line, = self.ax.plot(self.x_values, self.y_values, color='blue')

    def clear_plot(self):
        # Clear the current plot
        self.ax.clear()
        self.points = []  # Reset the points
        self.full_points = []

        # Load and resize the image background
        img = plt.imread(r"C:\Users\vihaa\FTC-Autonomous-Planner\FTC_Auto_Planner\MatPlotLibTests\background.jpg")

        # Set the image as the background
        self.ax.imshow(img, extent=[-10, 10, -10, 10])

        self.canvas.draw()

    def create_gui(self):
        # Create a Tkinter window
        window = tk.Tk()
        window.title("Matplotlib Graph in Tkinter")

        # Load and resize the image background
        img = plt.imread(r"C:\Users\vihaa\FTC-Autonomous-Planner\FTC_Auto_Planner\MatPlotLibTests\background.jpg")

        # Set the image as the background
        self.ax.imshow(img, extent=[-10, 10, -10, 10])

        # Create a canvas widget to display the graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create a toolbar for the graph
        toolbar = NavigationToolbar2Tk(self.canvas, window)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create buttons to interact with the plot
        self.marker_var = tk.StringVar()
        self.marker_var.set('*')  # Default marker

        circle_button = tk.Radiobutton(window, text="Start Point", variable=self.marker_var, value='*')
        circle_button.pack(side=tk.LEFT, padx=10)

        square_button = tk.Radiobutton(window, text="End Point", variable=self.marker_var, value='x')
        square_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(window, text="Clear", command=self.clear_plot)
        clear_button.pack(side=tk.LEFT, padx=10)

        # Bind the plot_data function to mouse clicks on the canvas
        self.canvas.mpl_connect('button_press_event', self.plot_data)

        # Run the Tkinter event loop
        window.mainloop()

    def return_points(self):

        self.full_points = []

        for value_num in range(len(self.x_values)):
            self.full_points.append([self.x_values[value_num], self.y_values[value_num]])
        
        return self.full_points


def plotter_main():
    # Create an instance of the Plotter class and run the GUI
    plotter = Plotter()
    plotter.create_gui()

plotter_main()

