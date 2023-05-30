import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from services.tacview_engine import process_all_tacview_files
from models.database import Database

import os


class TacviewGUIGrid:
    def __init__(self, db: Database):
        self.window = tk.Tk()
        self.window.title("Tacview2db")
        width = 750
        height = 730
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.window.geometry(alignstr)
        # self.window.resizable(width=False, height=False)

        self.clear_database_var = tk.BooleanVar()
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        # Label for files listbox
        lblFiles = tk.Label(self.window, text="Files for Processing", anchor="w")
        lblFiles.grid(row=0, column=0, padx=10, sticky="w")

        # File List Box
        self.lstFiles = tk.Listbox(self.window, selectmode=tk.MULTIPLE)
        self.lstFiles.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew"
        )

        # Open File Dialog Button
        btnOpen = tk.Button(
            self.window, text="Select Files", command=self.open_file_dialog
        )
        btnOpen.grid(row=1, column=2, padx=10, pady=5, sticky="nw")

        # Clear Files Button
        btnClear = tk.Button(self.window, text="Clear Files", command=self.clear_files)
        btnClear.grid(row=2, column=2, padx=10, pady=5, sticky="nw")

        # Clear Database Checkbox
        clear_database_checkbox = tk.Checkbutton(
            self.window,
            text="Clear Database before import",
            variable=self.clear_database_var,
        )
        clear_database_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Process Button
        btnProcess = tk.Button(
            self.window, text="Process Files", command=self.process_files
        )
        btnProcess.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Label for Log Messages
        lblLogMsgs = tk.Label(self.window, text="Log Messages", anchor="w")
        lblLogMsgs.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Logging window
        self.lstLogMsgs = tk.Text(self.window)
        self.lstLogMsgs.grid(row=5, column=0, padx=10, pady=5)

        # Progress Bar
        self.pgBar = Progressbar(self.window, mode="determinate")
        self.pgBar.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Quit Button
        btnQuit = tk.Button(self.window, text="Quit", command=self.window.quit)
        btnQuit.grid(row=7, column=2, padx=10, pady=10, sticky="e")

    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("XML Files", "*.xml")], multiple=True
        )
        for file_path in file_paths:
            self.lstFiles.insert(tk.END, file_path)

    def clear_files(self):
        self.lstFiles.delete(0, tk.END)

    def process_files(self):
        file_paths = self.lstFiles.get(0, tk.END)
        clear_database = self.clear_database_var.get()

        total_bytes = 0
        for file in file_paths:
            file_size = os.path.getsize(file)
            total_bytes += file_size
        self.pgBar["maximum"] = total_bytes

        # total_files = len(file_paths)
        # self.pgBar["maximum"] = total_files

        if clear_database:
            # Clear the database
            self.lstLogMsgs.insert(
                tk.END, "WARNING: Option to clear database selected.\n"
            )

        stats = process_all_tacview_files(self.db, clear_database, file_paths)

        for i, file_path in enumerate(file_paths, start=1):
            # Process the file
            result = f"Processing {file_path}...\n"
            self.lstLogMsgs.insert(tk.END, result)

            # Update progress bar
            self.pgBar["value"] = i
            self.window.update_idletasks()

    def run(self):
        self.window.mainloop()
