import pandas as pd
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile
import keyboard

# Global variables to control the playback
paused = False
position = 0
sample_rate = 44100
audio_signal = None

def toggle_pause(event):
    global paused
    paused = not paused
    if paused:
        stream.stop()
    else:
        stream.start()

def audio_callback(outdata, frames, time, status):
    global position, paused
    if status:
        print(status)
    if not paused:
        chunk = audio_signal[position:position + frames]
        if len(chunk) < len(outdata):
            outdata[:len(chunk)] = chunk.reshape(-1, 1)
            outdata[len(chunk):] = 0
            position = 0
            stream.stop()
            keyboard.unhook_all()  # Remove all keyboard event listeners
        else:
            outdata[:] = chunk.reshape(-1, 1)
            position += frames

def createWav():
    global audio_signal, sample_rate, position, stream  # Declare as global to access in toggle_pause

    df = pd.read_csv('ConvertedSheets/clean_audio.csv', skiprows=1)
    time = df.iloc[:, 0].to_numpy()  # First column
    # Convert scientific notation to standard notation
    time = np.array([float(i) for i in time])
    voltage = df.iloc[:, 1].to_numpy()  # Second column

    # Normalize the voltage data to map to a frequency range
    min_voltage = np.min(voltage)
    max_voltage = np.max(voltage)
    normalized_voltage = (voltage - min_voltage) / (max_voltage - min_voltage)
    frequency = 200 + normalized_voltage * (1700 - 200)  # Mapping to frequency

    # Generate the audio signal
    duration = 0.003  # Duration of the sound in seconds
    fade_duration = 0.003  # Duration of the fade in and fade out in seconds

    # Preallocate an array for the audio signal
    audio_signal = np.zeros(int(sample_rate * duration * len(frequency)))

    # Generate a time array and audio signal for each frequency
    for i, freq in enumerate(frequency):
        t = np.linspace(0, duration, int(sample_rate * duration), False)  # Time array
        signal = np.sin(2 * np.pi * freq * t)  # Generating the sine wave

        # Apply a fade in and fade out effect to avoid clicks at the beginning and end of the sound
        fade_in = np.linspace(0, 1, int(sample_rate * fade_duration))
        fade_out = np.linspace(1, 0, int(sample_rate * fade_duration))
        signal[:len(fade_in)] *= fade_in
        signal[-len(fade_out):] *= fade_out

        audio_signal[i*int(sample_rate * duration):(i+1)*int(sample_rate * duration)] = signal

    # Convert to 16-bit PCM format for sounddevice
    audio_signal = (audio_signal * 32767).astype(np.int16)

    # Visualize the voltage over time
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.title('Voltage over Time')
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.grid(True)
    plt.show()

    wavfile.write('clean_audio.wav', sample_rate, audio_signal)  # Write the audio signal to a WAV file

    # Set up the keyboard listener
    keyboard.on_press_key("space", toggle_pause)

    # Create an OutputStream with the audio callback
    stream = sd.OutputStream(callback=audio_callback, samplerate=sample_rate, channels=1, dtype='int16')
    stream.start()

def current_sound(current_position):
    df = pd.read_csv('ConvertedSheets/clean_audio.csv', skiprows=1)
    time = df.iloc[:, 0].to_numpy()  # First column
    # Convert scientific notation to standard notation
    time = np.array([float(i) for i in time])
    voltage = df.iloc[:, 1].to_numpy()  # Second column

    # Get the voltage at the current position
    voltage_at_position = voltage[current_position]

    # Normalize the voltage to a frequency
    min_voltage = np.min(voltage)
    max_voltage = np.max(voltage)
    normalized_voltage = (voltage_at_position - min_voltage) / (max_voltage - min_voltage)
    frequency = 200 + normalized_voltage * (1700 - 200)  # Mapping to frequency

    # Generate a sound wave
    sample_rate = 44100  # Sample rate in Hz
    duration = 1.0  # Duration of the sound in seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Play the sound
    sd.play(sound_wave, sample_rate)

    # Wait for the sound to finish playing
    sd.wait()
