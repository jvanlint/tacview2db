import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from services.tacview_engine import process_all_tacview_files


class TacviewGUI:
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

        self.clear_database_var = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        # Label for files listbox
        lblFiles = tk.Label(self.window, text="Files for Processing", anchor="w")
        lblFiles.place(x=10, y=10, width=200, height=30)

        # File List Box
        self.lstFiles = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        self.lstFiles.place(x=10, y=40, width=405, height=137)

        # Open File Dialog Button
        btnOpen = tk.Button(
            self.window, text="Select Files", command=self.open_file_dialog
        )
        btnOpen.place(x=420, y=40, width=110, height=30)

        # Clear Database Checkbox
        clear_database_checkbox = tk.Checkbutton(
            self.window,
            text="Clear Database before import",
            variable=self.clear_database_var,
        )
        clear_database_checkbox.place(x=10, y=200, width=279, height=32)

        # Process Button
        btnProcess = tk.Button(
            self.window, text="Process Files", command=self.process_files
        )
        btnProcess.place(x=10, y=250, width=403, height=32)

        # Label for Log Messages
        lblLogMsgs = tk.Label(self.window, text="Log Messages", anchor="w")
        lblLogMsgs.place(x=10, y=290, width=124, height=30)

        # Logging window
        self.lstLogMsgs = tk.Text(self.window)
        self.lstLogMsgs.place(x=10, y=320, width=404, height=181)

        # Progress Bar
        self.pgBar = Progressbar(self.window, mode="determinate", length=200)
        self.pgBar.pack(pady=10)

        # Quit Button
        btnQuit = tk.Button(self.window, text="Quit", command=self.window.quit)
        btnQuit.place(x=450, y=480, width=70, height=32)

    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("XML Files", "*.xml")])
        for file_path in file_paths:
            self.lstFiles.insert(tk.END, file_path)

    def process_files(self):
        file_paths = self.lstFiles.get(0, tk.END)
        clear_database = self.clear_database_var.get()

        total_files = len(file_paths)
        self.pgBar["maximum"] = total_files

        process_all_tacview_files("pytacview.db", clear_database, file_paths)

        if clear_database:
            # Clear the database
            self.lstLogMsgs.insert(tk.END, "Clearing the database...\n")

        for i, file_path in enumerate(file_paths, start=1):
            # Process the file
            result = f"Processing {file_path}...\n"
            self.lstLogMsgs.insert(tk.END, result)

            # Update progress bar
            self.pgBar["value"] = i
            self.window.update_idletasks()

    def run(self):
        self.window.mainloop()
