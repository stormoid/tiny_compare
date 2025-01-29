# -*- coding: utf-8 -*-

# Copyright 2025 stormoid
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import difflib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font


class DiffViewer:
    def __init__(self, master):
        self.master = master
        master.title("tiny_compare — stormoid")
        master.geometry("1600x900")

        self.initUI()

        self.left_file_path = ""
        self.right_file_path = ""

    def initUI(self):
        # File labels
        self.left_file_label = ttk.Label(self.master, text="File 1: None")
        self.left_file_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.right_file_label = ttk.Label(self.master, text="File 2: None")
        self.right_file_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # File buttons
        self.left_file_button = ttk.Button(
            self.master, text="Open File 1", command=self.open_left_file
        )
        self.left_file_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.right_file_button = ttk.Button(
            self.master, text="Open File 2", command=self.open_right_file
        )
        self.right_file_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Text areas
        self.left_text_frame = tk.Frame(self.master)
        self.left_text_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.left_text_frame.grid_rowconfigure(0, weight=1)  # Make text area expand vertically
        self.left_text_frame.grid_columnconfigure(0, weight=1) # Make text area expand horizontally
        
        self.left_text_edit = tk.Text(
            self.left_text_frame, wrap="none", state="disabled", bg="#f4f4f4" # Set background color
        )
        self.left_text_edit.grid(row=0, column=0, sticky="nsew")

        self.right_text_frame = tk.Frame(self.master)
        self.right_text_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.right_text_frame.grid_rowconfigure(0, weight=1) # Make text area expand vertically
        self.right_text_frame.grid_columnconfigure(0, weight=1) # Make text area expand horizontally

        self.right_text_edit = tk.Text(
            self.right_text_frame, wrap="none", state="disabled", bg="#f4f4f4" # Set background color
        )
        self.right_text_edit.grid(row=0, column=0, sticky="nsew")

        # Monospaced font
        mono_font = font.Font(family="Courier New", size=11)
        self.left_text_edit.configure(font=mono_font)
        self.right_text_edit.configure(font=mono_font)

        # Scrollbars
        self.left_vscrollbar = ttk.Scrollbar(
            self.left_text_frame, orient="vertical", command=self.left_text_edit.yview
        )
        self.left_vscrollbar.grid(row=0, column=1, sticky="ns")
        self.left_text_edit.configure(yscrollcommand=self.left_vscrollbar.set)

        self.left_hscrollbar = ttk.Scrollbar(
            self.left_text_frame, orient="horizontal", command=self.left_text_edit.xview
        )
        self.left_hscrollbar.grid(row=1, column=0, sticky="ew")
        self.left_text_edit.configure(xscrollcommand=self.left_hscrollbar.set)

        self.right_vscrollbar = ttk.Scrollbar(
            self.right_text_frame, orient="vertical", command=self.right_text_edit.yview
        )
        self.right_vscrollbar.grid(row=0, column=1, sticky="ns")
        self.right_text_edit.configure(yscrollcommand=self.right_vscrollbar.set)

        self.right_hscrollbar = ttk.Scrollbar(
            self.right_text_frame, orient="horizontal", command=self.right_text_edit.xview
        )
        self.right_hscrollbar.grid(row=1, column=0, sticky="ew")
        self.right_text_edit.configure(xscrollcommand=self.right_hscrollbar.set)

        # Tag configuration for highlighting
        self.left_text_edit.tag_configure("red", background="#ffaaaa")
        self.left_text_edit.tag_configure("yellow", background="#ffffaa")
        self.right_text_edit.tag_configure("green", background="#aaffaa")
        self.right_text_edit.tag_configure("yellow", background="#ffffaa")

        # Linked scrolling
        self.left_text_edit.configure(yscrollcommand=self.on_left_text_yscroll)
        self.left_text_edit.configure(xscrollcommand=self.on_left_text_xscroll)
        self.right_text_edit.configure(yscrollcommand=self.on_right_text_yscroll)
        self.right_text_edit.configure(xscrollcommand=self.on_right_text_xscroll)

        # Configure grid weights to allow resizing
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def on_left_text_yscroll(self, *args):
        self.left_vscrollbar.set(*args)
        self.right_text_edit.yview_moveto(args[0])

    def on_left_text_xscroll(self, *args):
        self.left_hscrollbar.set(*args)
        self.right_text_edit.xview_moveto(args[0])

    def on_right_text_yscroll(self, *args):
        self.right_vscrollbar.set(*args)
        self.left_text_edit.yview_moveto(args[0])

    def on_right_text_xscroll(self, *args):
        self.right_hscrollbar.set(*args)
        self.left_text_edit.xview_moveto(args[0])

    def open_left_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")],
        )
        if file_path:
            self.left_file_path = file_path
            self.left_file_label.config(text=f"File 1: {file_path}")
            self.compare_files()

    def open_right_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")],
        )
        if file_path:
            self.right_file_path = file_path
            self.right_file_label.config(text=f"File 2: {file_path}")
            self.compare_files()

    def compare_files(self):
        if not self.left_file_path or not self.right_file_path:
            return

        try:
            with open(self.left_file_path, "r") as f1, open(
                self.right_file_path, "r"
            ) as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
        except UnicodeDecodeError:
            self.left_text_edit.config(state="normal")
            self.left_text_edit.delete("1.0", tk.END)
            self.left_text_edit.insert(tk.END, "Error: Could not open file, binary or incompatible encoding detected in file 1.")
            self.left_text_edit.config(state="disabled")

            self.right_text_edit.config(state="normal")
            self.right_text_edit.delete("1.0", tk.END)
            self.right_text_edit.insert(tk.END, "Error: Could not open file, binary or incompatible encoding detected in file 2.")
            self.right_text_edit.config(state="disabled")
            return
        except Exception as e:
            self.left_text_edit.config(state="normal")
            self.left_text_edit.delete("1.0", tk.END)
            self.left_text_edit.insert(tk.END, f"Error: Could not open file 1. {e}")
            self.left_text_edit.config(state="disabled")

            self.right_text_edit.config(state="normal")
            self.right_text_edit.delete("1.0", tk.END)
            self.right_text_edit.insert(tk.END, f"Error: Could not open file 2. {e}")
            self.right_text_edit.config(state="disabled")
            return

        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        self.display_diff(diff, lines1, self.left_text_edit, True)
        self.display_diff(diff, lines2, self.right_text_edit, False)

    def display_diff(self, diff, original_lines, text_widget, is_left):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)

        line_num = 1
        for line in diff:
            line_code = line[:2]
            text = line[2:]

            if line_code == "  ":
                text_widget.insert(tk.END, f"{line_num:4}  {text}")
                line_num += 1
            elif line_code == "- " and is_left:
                text_widget.insert(tk.END, f"{line_num:4}  {text}", "red")
                line_num += 1
            elif line_code == "+ " and not is_left:
                text_widget.insert(tk.END, f"{line_num:4}  {text}", "green")
                line_num += 1
            elif line_code == "? ":
                if is_left:
                    text_widget.insert(tk.END, f"    ^{text[1:]}", "yellow")
                else:
                    text_widget.insert(tk.END, f"    ^{text[1:]}", "yellow")
            elif line_code == "+ " and is_left:  # Add blank lines in left for additions in right
                text_widget.insert(tk.END, "     \n") # No line number for blank lines
            elif line_code == "- " and not is_left:  # Add blank lines in right for deletions in left
                text_widget.insert(tk.END, "     \n") # No line number for blank lines
            else:
                pass

        text_widget.config(state="disabled")

def main():
    root = tk.Tk()
    viewer = DiffViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()