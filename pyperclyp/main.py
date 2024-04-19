#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pyperclyp -- Clipboard Manager using tkinter and pyperclip.

This module demonstrates creating a GUI application with tkinter that monitors
the system's clipboard, displaying each unique copied item in a list. Users can
double-click an item in the list to copy it back to the clipboard. Logging and
basic error handling are also demonstrated.
"""

__author__ = "Brad Kovaluk"
__email__ = "bkovaluk@gmail.com"
__date__ = "2024-04-10"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import messagebox
import pyperclip

# Configure basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ClipboardManager:
    """
    A class to manage and display the clipboard content using a GUI.

    Attributes:
        root (tk.Tk): The root window of the application.
        clipboard_contents (list of str): List to store unique clipboard items.
    """

    def __init__(self, root):
        """
        Initializes the ClipboardManager application.

        Parameters:
            root (tk.Tk): The root window for the application.
        """
        self.root = root
        self.clipboard_contents = []
        self._initialize_ui()

    def _initialize_ui(self):
        """Sets up the user interface of the application."""
        self.root.title("pyperclyp")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=10, pady=10)

        label = tk.Label(frame, text="Contents:", bg="#f0f0f0")
        label.grid(row=0, column=0)

        self.listbox = tk.Listbox(self.root, width=150, height=150)
        self.listbox.pack(pady=10)

        scrollbar = tk.Scrollbar(self.root, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind("<Double-Button-1>", self._copy_to_clipboard)
        self._update_listbox()

    def _update_listbox(self):
        """Checks the clipboard for new content and updates the listbox."""
        try:
            new_item = pyperclip.paste()
        except Exception as e:
            logging.error("Failed to access clipboard: %s", e)
            messagebox.showerror("Error", "Failed to access clipboard.")
            return

        if new_item not in self.clipboard_contents:
            self.clipboard_contents.append(new_item)
            self.listbox.insert(tk.END, new_item)
            self.listbox.insert(tk.END, "----------------------")
            logging.info("New clipboard item added.")

        self.listbox.yview(tk.END)
        self.root.after(1000, self._update_listbox)

    def _copy_to_clipboard(self, event):
        """
        Copies the selected item from the listbox back to the clipboard.

        Parameters:
            event: The event that triggered this callback.
        """
        selected_item = self.listbox.get(self.listbox.curselection())
        if selected_item:
            try:
                pyperclip.copy(selected_item)
                logging.info("Item copied to clipboard.")
            except Exception as e:
                logging.error("Failed to copy item to clipboard: %s", e)
                messagebox.showerror("Error", "Failed to copy item to clipboard.")


def main():
    """Runs the Clipboard Manager application."""
    root = tk.Tk()
    ClipboardManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
