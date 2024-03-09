import pandas as pd
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

df = pd.read_csv('ConvertedSheets\Audio2.csv')
time = df['Time'].to_numpy()
# Convert scientific notation to standard notation
time = np.array([float(i) for i in time])
voltage = df['Voltage'].to_numpy()

# Normalize the voltage data to map to a frequency range
min_voltage = np.min(voltage)
max_voltage = np.max(voltage)
normalized_voltage = (voltage - min_voltage) / (max_voltage - min_voltage)
frequency = 300 + normalized_voltage * (20)  # Mapping to frequency

# Generate the audio signal
sample_rate = 8000  # Sampling rate in Hz
t = np.linspace(0, len(time) / sample_rate, len(time), endpoint=False)  # Time array
audio_signal = np.sin(2 * np.pi * frequency * t)  # Generating the sine wave

# Convert to 16-bit PCM format for sounddevice
audio_signal = (audio_signal * 32767).astype(np.int16)

sd.play(audio_signal, sample_rate)

# Visualize the voltage over time
plt.figure(figsize=(10, 6))
plt.plot(time, voltage)
plt.title('Voltage over Time')
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.grid(True)
plt.show()

sd.wait()  # Wait until the sound has finished playing



