import tkinter as tk
from tkinter import filedialog
from csv_parser import clean_selected
from VoltAudio import createWav

file_path = ""

def button1_clicked():
    global file_path
    print("Button 1 clicked: csv_clean()")
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

def browse_button():
    global file_path
    file_path = str(filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")]))
    print("Selected file:", file_path)

# Create the main window
window = tk.Tk()
window.configure(bg="gray")
window.geometry("200x400")
window.title("VIOLET")

# Create the buttons
base_width = 10
base_height = 4
button1 = tk.Button(window, text="Button 1", command=button1_clicked, width=base_width, height=base_height)
button2 = tk.Button(window, text="Button 2", command=button2_clicked, width=base_width, height=base_height)
button3 = tk.Button(window, text="Button 3", command=button3_clicked, width=base_width, height=base_height)
# Create the browse button
browse_button = tk.Button(window, text="Browse", command=browse_button, width=base_width, height=base_height)

# Add the browse button to the window
# Align the buttons horizontally to the top of the window
button1.pack(side="top")
button2.pack(side="top")
button3.pack(side="top")
browse_button.pack(side="top")



# Start the main event loop
window.mainloop()
