import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar


def open_file_dialog():
    file_paths = filedialog.askopenfilenames(filetypes=[("XML Files", "*.xml")])
    for file_path in file_paths:
        file_list.insert(tk.END, file_path)


def process_files():
    file_paths = file_list.get(0, tk.END)
    clear_database = clear_database_var.get()
    display_log = display_log_var.get()

    total_files = len(file_paths)
    progress_bar["maximum"] = total_files

    if clear_database:
        # Clear the database
        result_box.insert(tk.END, "Clearing the database...\n")

    for i, file_path in enumerate(file_paths, start=1):
        # Process the file
        result = f"Processing {file_path}...\n"
        result_box.insert(tk.END, result)

        # Update progress bar
        progress_bar["value"] = i
        root.update_idletasks()

    if display_log:
        # Display log
        result_box.insert(tk.END, "Displaying log...\n")

    # Reset progress bar
    progress_bar["value"] = 0


root = tk.Tk()
root.title("File Processing Application")

# Frame to hold the buttons and file list
button_file_frame = tk.Frame(root)
button_file_frame.pack(pady=10)

# Open File Dialog Button
open_button = tk.Button(
    button_file_frame, text="Select Tacview XML Files", command=open_file_dialog
)
open_button.pack(side=tk.LEFT, padx=10)

# File List Box
file_list = tk.Listbox(button_file_frame, selectmode=tk.MULTIPLE, width=50)
file_list.pack(side=tk.LEFT, padx=10)

# Process Button
process_button = tk.Button(root, text="Process Files", command=process_files)
process_button.pack(pady=10)

# Label for Log Messages
log_label = tk.Label(root, text="Log Messages:")
log_label.pack()

# Result Box
result_box = tk.Text(root, height=10, width=50)
result_box.pack(pady=10)

# Checkboxes
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(anchor=tk.W)

clear_database_var = tk.BooleanVar()
clear_database_checkbox = tk.Checkbutton(
    checkbox_frame, text="Clear Database before import", variable=clear_database_var
)
clear_database_checkbox.pack(anchor=tk.W)

display_log_var = tk.BooleanVar()
display_log_checkbox = tk.Checkbutton(
    checkbox_frame, text="Display Log", variable=display_log_var
)
display_log_checkbox.pack(anchor=tk.W)

# Progress Bar
progress_bar = Progressbar(root, mode="determinate", length=200)
progress_bar.pack(pady=10)

# Quit Button
quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=10)

root.mainloop()
