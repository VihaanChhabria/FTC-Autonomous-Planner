import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math


class Plotter:
    def __init__(self):
        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.start_point = None
        self.waypoints = []
        self.end_point = None
        self.lines = []
        self.distances = []
        self.angles = []

        # Load the background image
        self.background_img = plt.imread(r'FTC_Auto_Planner\background.jpg')

    def plot_data(self, event):
        # Get the coordinates of the clicked point
        x = event.xdata
        y = event.ydata

        if x is not None and y is not None:
            # Get the current marker
            marker = self.marker_var.get()

            if marker == 'o':  # Start point
                self.start_point = (x, y)
            elif marker == 's':  # Waypoint
                self.waypoints.append((x, y))
            elif marker == '^':  # End point
                self.end_point = (x, y)

            # Plot the clicked point with the current marker and the same color
            self.ax.plot(x, y, marker=marker, color='red')

            # Plot or update the line passing through the points
            self.plot_line()

            self.canvas.draw()

    def plot_line(self):
        if self.start_point is not None and self.end_point is not None:
            # Clear the previous lines
            for line in self.lines:
                line.remove()
            self.lines.clear()

            # Extract x and y coordinates from the points
            x_values = [self.start_point[0]] + [point[0] for point in self.waypoints] + [self.end_point[0]]
            y_values = [self.start_point[1]] + [point[1] for point in self.waypoints] + [self.end_point[1]]

            # Plot the line passing through the points
            line, = self.ax.plot(x_values, y_values, color='blue')
            self.lines.append(line)

            # Calculate and store the distances and angles
            self.distances.clear()
            self.angles.clear()
            for i in range(len(x_values) - 2):
                distance = self.calculate_distance(x_values[i], y_values[i], x_values[i + 1], y_values[i + 1])
                angle = self.calculate_angle(x_values[i], y_values[i], x_values[i + 1], y_values[i + 1],
                                             x_values[i + 2], y_values[i + 2])
                self.distances.append(distance)
                self.angles.append(angle)

    def calculate_distance(self, x1, y1, x2, y2):
        # Calculate the Euclidean distance between two points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def calculate_angle(self, x1, y1, x2, y2, x3, y3):
        # Calculate the angle between three points using the dot product
        vector1 = [x1 - x2, y1 - y2]
        vector2 = [x3 - x2, y3 - y2]
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)
        angle_radians = math.acos(dot_product / (magnitude1 * magnitude2))
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def clear_plot(self):
        # Clear the current plot
        self.ax.clear()
        self.start_point = None
        self.waypoints = []
        self.end_point = None
        self.distances.clear()
        self.angles.clear()
        for line in self.lines:
            line.remove()
        self.lines.clear()
        self.canvas.draw()

    def create_gui(self):
        # Create a Tkinter window
        window = tk.Tk()
        window.title("Matplotlib Graph in Tkinter")

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
        self.marker_var.set('o')  # Default marker

        circle_button = tk.Radiobutton(window, text="Start Point", variable=self.marker_var, value='o')
        circle_button.pack(side=tk.LEFT, padx=10)

        square_button = tk.Radiobutton(window, text="Waypoint", variable=self.marker_var, value='s')
        square_button.pack(side=tk.LEFT, padx=10)

        triangle_button = tk.Radiobutton(window, text="End Point", variable=self.marker_var, value='^')
        triangle_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(window, text="Clear", command=self.clear_plot)
        clear_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(window, text="Save to File", command=self.save_to_file)
        save_button.pack(side=tk.LEFT, padx=10)

        rotate_button = tk.Button(window, text="Rotate Angle")

        rotate_textbox = tk.Entry(textvariable='test')
        rotate_textbox.pack(side=tk.LEFT, padx=10)

        # Bind the plot_data function to mouse clicks on the canvas
        self.canvas.mpl_connect('button_press_event', self.plot_data)

        # Display the background image
        self.ax.imshow(self.background_img, extent=[0, 144, 0, 144])

        # Run the Tkinter event loop
        window.mainloop()

    

    def save_to_file(self):
        # Read the contents of the demofile.java file
        with open(r'FTC_Auto_Planner\demofile.java', 'r') as file:
            lines = file.readlines()

        # Find the index of the line where you want to insert the information
        insert_index = lines.index("        //Test\n") + 1

        # Insert the line information at the specified index
        lines.insert(insert_index, "\n")
        for distance, angle in zip(self.distances, self.angles):
            lines.insert(insert_index, f"        drivetrain.DrivetrainAutoMove({distance}, 0.75, {angle}, telemetry);\n")

        # Write the modified lines back to the demofile.java file
        with open(r'FTC_Auto_Planner\demofile.java', 'w') as file:
            file.writelines(lines)


# Create an instance of the Plotter class and run the GUI
plotter = Plotter()
plotter.create_gui()
