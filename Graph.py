import matplotlib.pyplot as plt

class LivePlotter:
    def __init__(self):
        self.ph_data = []
        self.x_data = []

        plt.ion()  # Enable interactive mode
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.x_data, self.ph_data)

        self.ax.set_xlabel('Data Point')
        self.ax.set_ylabel('pH')

    def update_plot(self, x_value, ph_value):
        self.x_data.append(x_value)
        self.ph_data.append(ph_value)

        self.line.set_data(self.x_data, self.ph_data)

        self.ax.relim()
        self.ax.autoscale_view()

        plt.draw()
        plt.pause(0.1)

