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
        self.intake_state = 1

        self.distances = []
        self.angles = []

        self.arm_count = 0

        # Load the background image
        self.background_img = plt.imread(r'FTC_Auto_Planner\background.jpg')

    def neg_clicked(self):
        self.arm_count -= 1

        self.pos['text'] = str(self.arm_count)

    def pos_clicked(self):
        self.arm_count += 1

        self.pos['text'] = str(self.arm_count)

    def arm_position_popup(self):
        popup = tk.Tk()
        popup.wm_title("Select Arm Position")

        label = tk.Label(popup, text="Select Arm Position")
        label.pack(side="top", fill="x", pady=10)

        self.pos = tk.Label(popup, text="0")
        self.pos.pack(side="top", fill="x", pady=10)

        self.pos_button = tk.Button(popup, text="Increase", command=self.pos_clicked)
        self.pos_button.pack(side="left", fill="x", pady=10)

        self.neg_button = tk.Button(popup, text="Decrease", command=self.neg_clicked)
        self.neg_button.pack(side="right", fill="x", pady=10)

        popup.mainloop()


    def plot_data(self, event):
        # Get the coordinates of the clicked point
        x = int(event.xdata)
        y = int(event.ydata)

        if x is not None and y is not None:
            # Get the current marker
            marker = self.marker_var.get()

            if marker == 'o':  # Start point
                self.start_point = (x, y)
            elif marker == 's':  # Waypoint
                point = (x, y)
                #if self.waypoints == []:
                self.waypoints.append([point, self.intake_state, self.arm_count])

                if len(self.waypoints) >= 2:
                    if self.waypoints[-1] == self.waypoints[-2]:
                        self.waypoints.pop()

            elif marker == '^':  # End point
                self.end_point = (x, y)

            # Plot the clicked point with the current marker and the same color
            self.ax.plot(x, y, marker=marker, color='red')

            # Plot or update the line passing through the points
            self.plot_line()

            self.canvas.draw()

            # Update the point list after adding the point
            self.update_point_list()

    def plot_line(self):
        if self.start_point is not None and self.end_point is not None:
            # Clear the previous lines
            for line in self.lines:
                line.remove()
            self.lines.clear()

            # Extract x and y coordinates from the points
            x_values = [self.start_point[0]] + [point[0][0] for point in self.waypoints] + [self.end_point[0]]
            y_values = [self.start_point[1]] + [point[0][1] for point in self.waypoints] + [self.end_point[1]]

            # Plot the line passing through the points
            line, = self.ax.plot(x_values, y_values, color='blue')
            self.lines.append(line)

    def clear_plot(self):
        # Clear the current plot
        self.ax.clear()
        self.start_point = None
        self.waypoints = []
        self.end_point = None

        self.distances = []
        self.angles = []
        for line in self.lines:
            line.remove()

        self.ax.imshow(self.background_img, extent=[0, 144, 0, 144])
        self.point_listbox.delete(0, tk.END)
        
        self.lines.clear()
        self.canvas.draw()

    def create_gui(self):
        # Create a Tkinter window
        window = tk.Tk()
        window.title("Matplotlib Graph in Tkinter")

        # Create a frame to hold the listbox
        frame = tk.Frame(window)
        frame.pack(side=tk.TOP)

        # Create a listbox to display the point list
        self.point_listbox = tk.Listbox(frame)
        self.point_listbox.pack(side=tk.LEFT)

        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the listbox to use the scrollbar
        self.point_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.point_listbox.yview)

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

        start_button = tk.Radiobutton(window, text="Start Point", variable=self.marker_var, value='o')
        start_button.pack(side=tk.LEFT, padx=10)

        way_button = tk.Radiobutton(window, text="Waypoint", variable=self.marker_var, value='s')
        way_button.pack(side=tk.LEFT, padx=10)

        end_button = tk.Radiobutton(window, text="End Point", variable=self.marker_var, value='^')
        end_button.pack(side=tk.LEFT, padx=10)

        intake_button = tk.Button(window, text="Intake Toggle", command=self.change_intake)
        intake_button.pack(side=tk.LEFT, padx=10)

        intake_button = tk.Button(window, text="Clear", command=self.clear_plot)
        intake_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(window, text="Save to File", command=self.save_to_file)
        save_button.pack(side=tk.LEFT, padx=10)

        arm_button = tk.Button(window, text="Arm", command=self.arm_position_popup)
        arm_button.pack(side=tk.LEFT, padx=10)

        # Bind the plot_data function to mouse clicks on the canvas
        self.canvas.mpl_connect('button_press_event', self.plot_data)

        # Display the background image
        self.ax.imshow(self.background_img, extent=[0, 144, 0, 144])

        # Update the point list initially
        self.update_point_list()

        # Update the point list after each point is added
        def update_list_after_plot(event):
            self.plot_data(event)
            self.update_point_list()

        self.canvas.mpl_connect('button_release_event', update_list_after_plot)

        # Run the Tkinter event loop
        window.mainloop()

    def change_intake(self):
        self.intake_state = self.intake_state * -1

    def calculate_distance(self, coord1, coord2):
        # Calculate the Euclidean distance between two points
        distance = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
        return distance

    def calculate_angle(self, coord1, coord2):
        dx = coord1[1] - coord1[0]
        dy = coord2[1] - coord2[0]
        angle = math.atan2(dy, dx)  # Calculate the angle in radians
        angle_deg = math.degrees(angle)  # Convert the angle to degrees
        if angle_deg < 0:
            angle_deg += 360  # Normalize the angle between 0 and 360 degrees
        return angle_deg

    def update_point_list(self):
        # Clear the existing items in the listbox
        self.point_listbox.delete(0, tk.END)

        # Add the start point to the listbox
        if self.start_point is not None:
            self.point_listbox.insert(tk.END, f"Start Point: {self.start_point}")

        # Add the waypoints to the listbox
        for i, waypoint in enumerate(self.waypoints):
            #if ((abs((waypoint[0][0]) - self.waypoints[i-1][0][0]) < 5)) and ((abs((waypoint[0][1]) - self.waypoints[i-1][0][1]) < 5)):
            #    continue
            self.point_listbox.insert(tk.END, f"Waypoint {i + 1}: {waypoint[0]}")
            self.point_listbox.insert(tk.END, f"Intake Status: {waypoint[1]}")
            self.point_listbox.insert(tk.END, f"Arm Status: {waypoint[2]}")

        # Add the end point to the listbox
        if self.end_point is not None:
            self.point_listbox.insert(tk.END, f"End Point: {self.end_point}")

    def save_to_file(self):
        # Calculate and store the distances and angles
        self.distances.clear()
        self.angles.clear()

        self.full_points = self.waypoints
        self.full_points.insert(0, (self.start_point, 1))
        self.full_points.append((self.end_point, 1))

        for point_index, point in enumerate(self.full_points):
            if point == self.full_points[-1]:
                continue

            distance = self.calculate_distance(point[0], self.full_points[point_index+1][0])
            angle = self.calculate_angle(point[0], self.full_points[point_index+1][0])

            self.distances.append(distance)
            self.angles.append(angle)


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
