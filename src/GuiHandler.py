import tkinter as tk
from tkinter import PhotoImage, filedialog
from csv_parser import clean_selected
from VoltAudio import create_wav, current_sound, play_full
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import pyttsx3
import speech_recognition as sr
import threading

file_path = ""
listening_event = threading.Event()
recognition_thread = None
recognizer = sr.Recognizer()

# Initialize TTS engine
tts_engine = pyttsx3.init()

def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_and_recognize():
    global recognition_thread
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        text_to_speech("Listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
            recognition_thread = threading.Thread(target=recognize_speech, args=(audio,), daemon=True)
            recognition_thread.start()
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")

def recognize_speech(audio):
    try:
        text_to_speech("Recognizing...")
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        process_command(text.lower())
    except sr.UnknownValueError:
        text_to_speech("Sorry, I did not understand that.")
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        text_to_speech("Could not request results from the speech recognition service.")
        print("Could not request results from the speech recognition service.")

def process_command(command):
    if "browse" in command:
        browse_button()
    elif "generate" in command:
        generate_clicked()
    elif "replay" in command:
        replay_clicked()
    elif "open graph" in command:
        open_graph_in_main_window()
    elif "go left" in command and graph_displayed:
        navigate_left()
    elif "go right" in command and graph_displayed:
        navigate_right()
    elif "play sound" in command and graph_displayed:
        play_current_sound()
    elif "exit" in command or "quit" in command:
        text_to_speech("Exiting application")
        window.quit()

# Callback function for the browse button
def browse_button():
    global file_path
    file_path = str(filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")]))
    print("Selected file:", file_path)
    text_to_speech(f"Selected file")

# Callback function for the generate button
def generate_clicked():
    global file_path
    print("Generate button clicked: Generating wav file")
    print("File path:", file_path)
    if file_path == "":
        print("No file selected")
        text_to_speech("No file selected")
        # Create a dialog box with the message "No file selected"
        dialog_box = tk.Toplevel(window)
        dialog_box.title("No file selected")
        dialog_box.geometry("200x100")
        
        # Create a label with the message
        label = tk.Label(dialog_box, text="No file selected")
        label.pack(pady=20)
        
        # Create a button to close the dialog box
        ok_button = tk.Button(dialog_box, text="OK", command=dialog_box.destroy)
        ok_button.pack()
    else:
        clean_selected(file_path)
        create_wav()

def replay_clicked():
    print("Replay button clicked: playFull()")
    play_full()

def play_current_sound(event=None):
    global current_point_index
    current_sound(current_point_index)

def navigate_left(event=None):
    global current_point_index
    if current_point_index > 0:
        current_point_index -= 1
        update_current_point()

def navigate_right(event=None):
    global current_point_index
    if current_point_index < len(x) - 1:
        current_point_index += 1
        update_current_point()

def update_current_point():
    global current_point_index, x, y, ax, canvas, current_point_label
    # Update the label text
    current_point_label.config(text=f"Current point index: {current_point_index}")
    # Redraw the plot with the current point highlighted
    ax.clear()
    ax.plot(x, y)
    ax.plot(x[current_point_index], y[current_point_index], 'ro')
    canvas.draw()

def open_graph_in_main_window():
    global x, y, ax, canvas, current_point_label, current_point_index, graph_displayed
    if graph_displayed:
        text_to_speech("Graph is already displayed")
        return

    df = pd.read_csv('ConvertedSheets/clean_audio.csv')
    x = df.iloc[:, 0] 
    y = df.iloc[:, 1] 

    # Create a figure and a plot
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    # Create a canvas and add it to the main window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a label to display the current point
    current_point_index = 0
    current_point_label = tk.Label(window, text=f"Current point index: {current_point_index}")
    current_point_label.pack()

    # Bind the arrow keys to navigation and sound
    window.bind('<Left>', navigate_left)
    window.bind('<Right>', navigate_right)
    window.bind('<Up>', play_current_sound)
    graph_displayed = True

def listen_for_commands():
    while listening_event.is_set():
        listen_and_recognize()

def start_listening(event):
    global listening_thread
    if not listening_event.is_set():
        listening_event.set()
        listening_thread = threading.Thread(target=listen_for_commands, daemon=True)
        listening_thread.start()

def stop_listening(event):
    if listening_event.is_set():
        listening_event.clear()
        if listening_thread is not None:
            listening_thread.join()

# Main window configuration
window = tk.Tk()
window.configure(bg="gray")
window.title("VIOLET")
icon_path = "icon.png" 
icon = PhotoImage(file=icon_path)
window.iconphoto(False, icon)

graph_displayed = False

# Bind the spacebar key events so that the application listens for voice commands while space is held down
window.bind('<space>', start_listening)
window.bind('<KeyRelease-space>', stop_listening)

# Create the buttons
base_width = 10
base_height = 4

browse_button = tk.Button(window, text="Browse", command=browse_button, width=base_width, height=base_height)
generate_button = tk.Button(window, text="Generate", command=generate_clicked, width=base_width, height=base_height)
replay_button = tk.Button(window, text="Replay", command=replay_clicked, width=base_width, height=base_height)

# Align the buttons
browse_button.pack(side="top")
generate_button.pack(side="top")
replay_button.pack(side="top")

open_graph_button = tk.Button(window, text="Open Graph", command=open_graph_in_main_window, width=base_width, height=base_height)
open_graph_button.pack(side="top")

# Start the main event loop
window.mainloop()
