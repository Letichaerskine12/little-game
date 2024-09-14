import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Manager")

        # Data lists
        self.all_texts = []
        self.emails = []
        self.last_clipboard = ""

        # Create the Notebook (tabs container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create frames for each tab
        self.all_frame = ttk.Frame(self.notebook, width=400, height=280)
        self.email_frame = ttk.Frame(self.notebook, width=400, height=280)
        self.password_frame = ttk.Frame(self.notebook, width=400, height=280)

        self.all_frame.pack(fill='both', expand=True)
        self.email_frame.pack(fill='both', expand=True)
        self.password_frame.pack(fill='both', expand=True)

        # Add frames to notebook
        self.notebook.add(self.all_frame, text='All Texts')
        self.notebook.add(self.email_frame, text='Emails')
        self.notebook.add(self.password_frame, text='Generate Password')

        # All Texts tab
        self.all_listbox = tk.Listbox(self.all_frame)
        self.all_listbox.pack(pady=20)
        self.all_listbox.bind("<Double-1>", self.copy_from_listbox)

        # Emails tab
        self.email_listbox = tk.Listbox(self.email_frame)
        self.email_listbox.pack(pady=20)
        self.email_listbox.bind("<Double-1>", self.copy_from_listbox)

        # Generate Password tab
        self.create_password_tab()

        # Regularly check clipboard
        self.check_clipboard()

        # Clear button
        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_data)
        self.clear_button.pack(pady=10)

    def create_password_tab(self):
        self.letters_var = tk.BooleanVar()
        self.digits_var = tk.BooleanVar()
        self.symbols_var = tk.BooleanVar()
        self.length_var = tk.IntVar(value=8)

        ttk.Checkbutton(self.password_frame, text="Include Letters", variable=self.letters_var).pack(pady=5)
        ttk.Checkbutton(self.password_frame, text="Include Digits", variable=self.digits_var).pack(pady=5)
        ttk.Checkbutton(self.password_frame, text="Include Symbols", variable=self.symbols_var).pack(pady=5)

        tk.Label(self.password_frame, text="Password Length:").pack(pady=5)
        tk.Scale(self.password_frame, from_=4, to_=32, orient='horizontal', variable=self.length_var).pack(pady=5)

        ttk.Button(self.password_frame, text="Generate Password", command=self.generate_password).pack(pady=10)

        self.password_listbox = tk.Listbox(self.password_frame)
        self.password_listbox.pack(pady=10)
        self.password_listbox.bind("<Double-1>", self.copy_from_listbox)

    def check_clipboard(self):
        try:
            current_clipboard = self.root.clipboard_get()
            if current_clipboard != self.last_clipboard:
                self.on_paste(current_clipboard)
                self.last_clipboard = current_clipboard
        except tk.TclError:
            pass
        self.root.after(1000, self.check_clipboard)  # check every second

    def on_paste(self, text):
        if text and text not in self.all_texts:
            self.all_texts.append(text)
            self.all_listbox.insert(tk.END, text)
            if re.match(r"[^@]+@[^@]+\.[^@]+", text):
                self.emails.append(text)
                self.email_listbox.insert(tk.END, text)

    def copy_from_listbox(self, event):
        try:
            selected_text = event.widget.get(event.widget.curselection())
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            messagebox.showinfo('Copied', 'The text has been copied to clipboard.')
        except tk.TclError:
            messagebox.showwarning('Warning', 'No item selected.')

    def generate_password(self):
        chars = ""
        if self.letters_var.get():
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.digits_var.get():
            chars += "0123456789"
        if self.symbols_var.get():
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

        if chars:
            length = self.length_var.get()
            password = ''.join(random.choice(chars) for _ in range(length))
            self.password_listbox.insert(tk.END, password)
        else:
            messagebox.showwarning("Warning", "Please select at least one option for password generation.")

    def clear_data(self):
        self.all_texts.clear()
        self.emails.clear()
        self.all_listbox.delete(0, tk.END)
        self.email_listbox.delete(0, tk.END)
        self.password_listbox.delete(0, tk.END)
        messagebox.showinfo('Cleared', 'All data has been cleared.')

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()
