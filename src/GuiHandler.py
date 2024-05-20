import tkinter as tk
from tkinter import filedialog
from csv_parser import clean_selected
from VoltAudio import createWav, current_sound
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

file_path = ""

# Callback function for the browse button, this will open a file dialog to select a csv file
def browse_button():
    global file_path
    file_path = str(filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")]))
    print("Selected file:", file_path)

# Callback function for the generate button, this will generate a wav file based on the selected csv file
def generate_clicked():
    global file_path
    print("Generate button clicked: Generating wav file")
    print("File path:", file_path)
    if file_path == None:
        print("No file selected")
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
        createWav()
def button2_clicked():
    print("Button 2 clicked: createWav()")
def button3_clicked():
    print("Button 3 clicked")



# Create the main window
window = tk.Tk()
window.configure(bg="gray")
# window.geometry("200x400")
window.title("VIOLET")

# Create the buttons
base_width = 10
base_height = 4

browse_button = tk.Button(window, text="Browse", command=browse_button, width=base_width, height=base_height)
generate_button = tk.Button(window, text="Generate", command=generate_clicked, width=base_width, height=base_height)
button2 = tk.Button(window, text="Button 2", command=button2_clicked, width=base_width, height=base_height)
button3 = tk.Button(window, text="Button 3", command=button3_clicked, width=base_width, height=base_height)

# Current point index
current_point_index = 0

def play_current_sound(event):
    global current_point_index
    current_sound(current_point_index)

def navigate_left(event):
    global current_point_index
    if current_point_index > 0:
        current_point_index -= 1
        update_current_point()

def navigate_right(event):
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

def open_graph_window():
    global x, y, ax, canvas, current_point_label, current_point_index
    # Create a new window
    graph_window = tk.Toplevel(window)

    # Load the data
    df = pd.read_csv('ConvertedSheets/clean_audio.csv')
    x = df.iloc[:, 0] 
    y = df.iloc[:, 1] 

    # Create a figure and a plot
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    # Create a canvas and add it to the window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Add a label to display the current point
    current_point_index = 0
    current_point_label = tk.Label(graph_window, text=f"Current point index: {current_point_index}")
    current_point_label.pack()

    # Bind the left and right arrow keys
    graph_window.bind('<Left>', navigate_left)
    graph_window.bind('<Right>', navigate_right)
    graph_window.bind('<Up>', play_current_sound)

# Add the browse button to the window
# Align the buttons horizontally to the top of the window
generate_button.pack(side="top")
# button2.pack(side="top")
# button3.pack(side="top")
browse_button.pack(side="top")
# Create a button that opens the graph window
open_graph_button = tk.Button(window, text="Open Graph", command=open_graph_window, width=base_width, height=base_height)
open_graph_button.pack(side="top")

# Start the main event loop
window.mainloop()