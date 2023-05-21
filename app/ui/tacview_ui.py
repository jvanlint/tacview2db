import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar


class TacviewUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tacview2db")
        width = 540
        height = 540
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)

        # Label for files listbox
        self.files_label = tk.Label(
            self.window, text="Files for Processing", anchor="w"
        )
        self.files_label.place(x=10, y=10, width=200, height=30)

        # Open File Dialog Button
        self.open_button = tk.Button(
            self.window, text="Select Files", command=self.open_file_dialog
        )
        # open_button.pack(side=tk.LEFT, padx=10)
        self.open_button.place(x=420, y=40, width=110, height=30)

        # File List Box
        self.file_list = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        self.file_list.place(x=10, y=40, width=405, height=137)

        # Process Button
        self.process_button = tk.Button(
            self.window, text="Process Files", command=self.process_files
        )
        self.process_button.place(x=10, y=250, width=403, height=32)

        # Label for Log Messages
        self.log_label = tk.Label(self.window, text="Log Messages", anchor="w")
        self.log_label.place(x=10, y=290, width=124, height=30)

        # Result Box
        self.result_box = tk.Text(self.window)
        self.result_box.place(x=10, y=320, width=404, height=181)

        clear_database_var = tk.BooleanVar()
        clear_database_checkbox = tk.Checkbutton(
            self.window,
            text="Clear Database before import",
            variable=clear_database_var,
            anchor="w",
        )
        clear_database_checkbox.place(x=20, y=180, width=279, height=32)

        display_log_var = tk.BooleanVar()
        display_log_checkbox = tk.Checkbutton(
            self.window, text="Display Log", variable=display_log_var, anchor="w"
        )
        display_log_checkbox.place(x=20, y=210, width=200, height=25)

        # Progress Bar
        progress_bar = Progressbar(self.window, mode="determinate", length=200)
        progress_bar.pack(pady=10)

        # Quit Button
        quit_button = tk.Button(self.window, text="Quit", command=self.window.quit)
        quit_button.place(x=450, y=480, width=70, height=32)

        self.window.mainloop()

    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("XML Files", "*.xml")])
        for file_path in file_paths:
            self.file_list.insert(tk.END, file_path)

    def process_files(self):
        file_paths = self.file_list.get(0, tk.END)
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
