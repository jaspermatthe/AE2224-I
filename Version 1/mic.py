import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import hann, butter, lfilter

# Load data from Excel sheet
data2 = pd.read_excel('Averaged Data b15.xlsx')
file_pattern = 'b15_Run{}.xlsx'

# Set the number of blades
B = 3   

# Set the delta_f and p0 values for SPSL calculation
delta_f = 0.2
p0 = 2e-5
# Set the sampling frequency
fs = 51200

run_number = 1
# Generate the file name for the current data sheet
file_name = file_pattern.format(run_number)

# Load data from Excel sheet
data = pd.read_excel(file_name)

# Set the blade rotational speed
omega = data2.values[run_number, 7] /   2 * np.pi

# Define filter parameters
cutoff_freq = 100
order = 4

# Iterate over the columns containing microphone data
for column in data.columns[0:1]:
    # Extract the pressure values from the column
    pressure_data = data[column].values
    print(len(pressure_data))

    # Apply Hanning window
    pressure_data *= hann(len(pressure_data))

    # Apply low pass filter
    w_cutoff = 2 * cutoff_freq / fs
    b, a = butter(order, w_cutoff, 'low')
    pressure_data = lfilter(b, a, pressure_data)

    # Perform FFT
    fft_data = fft(pressure_data)
    fft_data = np.abs(fft_data[:len(fft_data)//2])  # Discard negative frequencies

    # Compute the power spectral density (PSD)
    psd = (fft_data ** 2) / (fs * len(pressure_data))

    # Compute frequency axis
    freqs = fftfreq(len(pressure_data), 1 / fs)
    freqs = freqs[:len(freqs)//2]  # Discard negative frequencies

    # Calculate harmonics of Blade Passing Frequency (HBPF)
    hbpf = (2 * np.pi * freqs) / (B * omega)

    # Calculate Sound Pressure Spectrum Level (SPSL)
    spsl = 10 * np.log10(psd * delta_f / p0**2)

    # Set a filter to exclude HBPF values close to 0
    hbpf_threshold = 1e-3  # Adjust the threshold as needed
    filtered_hbpf = hbpf[abs(hbpf) > hbpf_threshold]
    filtered_spsl = spsl[abs(hbpf) > hbpf_threshold]

    # Plot the filtered SPSL - HBPF diagram for each microphone
    plt.plot(filtered_hbpf, filtered_spsl, label='Microphone {}'.format(column))

# Set the plot labels and legend
plt.xlabel('Harmonics of Blade Passing Frequency (HBPF)')
plt.xlim(0.6,10)
plt.x_scale = 'log'
plt.ylabel('Sound Pressure Spectrum Level (dB)')
plt.title('SPSL - HBPF Diagram for 9 Microphones')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
