import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FixedFormatter

# Generate some example data
x = np.logspace(0, 3, 100)
y = np.random.rand(100)

# Create the plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xscale('log')

# Define the locations and labels for the ticks
tick_locs = [1, 10, 100, 500, 1000]
tick_labels = ['1', '10', '100', '500', '1000']

# Set the tick locations and labels
ax.xaxis.set_major_locator(LogLocator(subs=(1.0,)))
ax.xaxis.set_minor_locator(LogLocator(subs=np.arange(2, 10) * 0.1))
ax.xaxis.set_major_formatter(FixedFormatter(tick_labels))
ax.tick_params(which='both', direction='in')

# Set the axis labels and title
ax.set_xlabel('Harmonics of Blade Passing Frequency (HBPF)')
ax.set_ylabel('Sound Pressure Spectrum Level (dB)')
ax.set_title('SPSL - HBPF Diagram for 9 Microphones')
ax.grid(True)

# Show the plot
plt.show()
