import pandas as pd
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile

stretch_scalar = input("Enter the amount of horizontal stretch, skip for none: ")
if stretch_scalar == None:
    stretch_scalar = 1
else:
    stretch_scalar = int(stretch_scalar)

pitch_scalar = input("Enter the amount of pitch increase, skip for none: ")
if pitch_scalar == None:
    pitch_scalar = 1
else:
    pitch_scalar = float(pitch_scalar)

df = pd.read_csv('ConvertedSheets/sawtooth csv.csv', skiprows=1)
time = df.iloc[:, 0].to_numpy()  # First column
# Convert scientific notation to standard notation
time = np.array([float(i) for i in time])
voltage = df.iloc[:, 1].to_numpy()  # Second column

# Stretch the time and voltage arrays
time = np.repeat(time, stretch_scalar)
voltage = np.repeat(voltage, stretch_scalar)

# Normalize the voltage data to map to a frequency range
min_voltage = np.min(voltage)
max_voltage = np.max(voltage)
normalized_voltage = (voltage - min_voltage) / (max_voltage - min_voltage)
frequency = 300 + normalized_voltage * (20)  # Mapping to frequency

frequency = frequency * pitch_scalar

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

wavfile.write('sawtooth.wav', sample_rate, audio_signal)  # Write the audio signal to a WAV file

sd.wait()  # Wait until the sound has finished playing



