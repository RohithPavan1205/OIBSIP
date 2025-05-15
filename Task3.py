import tkinter as tk
from tkinter import messagebox
import random
import string

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("450x350")
        self.root.config(padx=20, pady=20)

        self.len_var = tk.StringVar(value="12")
        self.up_var = tk.BooleanVar(value=True)
        self.low_var = tk.BooleanVar(value=True)
        self.dig_var = tk.BooleanVar(value=True)
        self.sym_var = tk.BooleanVar(value=True)
        self.exc_var = tk.StringVar(value="")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Password Length (8-128):").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.len_var, width=10).grid(row=0, column=1, sticky="w")

        tk.Checkbutton(self.root, text="Include Uppercase (A-Z)", variable=self.up_var).grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(self.root, text="Include Lowercase (a-z)", variable=self.low_var).grid(row=2, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(self.root, text="Include Digits (0-9)", variable=self.dig_var).grid(row=3, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(self.root, text="Include Symbols (!@#$...) ", variable=self.sym_var).grid(row=4, column=0, columnspan=2, sticky="w")

        tk.Label(self.root, text="Exclude Characters:").grid(row=5, column=0, sticky="w", pady=(10,0))
        tk.Entry(self.root, textvariable=self.exc_var, width=30).grid(row=5, column=1, sticky="w", pady=(10,0))

        tk.Button(self.root, text="Generate Password", command=self.gen_pass, bg="#0078D7", fg="white").grid(row=6, column=0, columnspan=2, pady=15)

        self.pass_box = tk.Text(self.root, height=2, width=40, font=("Segoe UI", 12))
        self.pass_box.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_pass).grid(row=8, column=0, columnspan=2)

    def gen_pass(self):
        try:
            length = int(self.len_var.get())
            if length < 8 or length > 128:
                raise ValueError("Password length must be between 8 and 128.")

            pools = []
            if self.up_var.get():
                pools.append(string.ascii_uppercase)
            if self.low_var.get():
                pools.append(string.ascii_lowercase)
            if self.dig_var.get():
                pools.append(string.digits)
            if self.sym_var.get():
                pools.append("!@#$%^&*()-_=+[]{}|;:,.<>?/")

            if not pools:
                raise ValueError("Select at least one character type.")

            exc = set(self.exc_var.get())

            filtered = []
            for pool in pools:
                f = ''.join([c for c in pool if c not in exc])
                if f:
                    filtered.append(f)
                else:
                    raise ValueError("Excluding too many characters leaves no options for a character set.")

            pass_chars = [random.choice(p) for p in filtered]

            all_chars = ''.join(filtered)
            if len(all_chars) == 0:
                raise ValueError("No characters left to generate password after exclusion.")

            left = length - len(pass_chars)
            pass_chars += random.choices(all_chars, k=left)

            random.shuffle(pass_chars)

            password = ''.join(pass_chars)

            self.pass_box.delete("1.0", tk.END)
            self.pass_box.insert(tk.END, password)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def copy_pass(self):
        pwd = self.pass_box.get("1.0", tk.END).strip()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
