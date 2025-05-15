import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import json
import os
import matplotlib.pyplot as plt

DATA_FILE = "bmi_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        bmi_data = json.load(f)
else:
    bmi_data = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(bmi_data, f, indent=4)

def calculate_bmi():
    user = user_var.get().strip()
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        if weight < 10 or weight > 500 or height_cm < 50 or height_cm > 300:
            raise ValueError("Please enter realistic weight and height values.")

        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"BMI: {bmi} ({category})", fg="blue")

        record = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "weight": weight,
            "height": height_cm,
            "bmi": bmi,
        }

        bmi_data.setdefault(user, []).append(record)
        save_data()

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def view_history():
    user = user_var.get().strip()
    history = bmi_data.get(user, [])
    if not history:
        messagebox.showinfo("No Data", "No history found for this user.")
        return

    lines = [f"{h['date']} - BMI: {h['bmi']} (Weight: {h['weight']}kg, Height: {h['height']}cm)" for h in history]
    messagebox.showinfo(f"{user}'s BMI History", "\n".join(lines))

def show_graph():
    user = user_var.get().strip()
    history = bmi_data.get(user, [])
    if not history:
        messagebox.showinfo("No Data", "No BMI records to display.")
        return

    dates = [h["date"] for h in history]
    bmis = [h["bmi"] for h in history]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, 'go-', linewidth=2)
    plt.title(f"{user}'s BMI Trend")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def select_user():
    name = simpledialog.askstring("User", "Enter your name:")
    if name:
        user_var.set(name.strip())

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x350")
root.config(bg="#f0f0f0")

label_font = ("Segoe UI", 11)
entry_font = ("Segoe UI", 11)
btn_font = ("Segoe UI", 10, "bold")

tk.Label(root, text="User Name:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
user_var = tk.StringVar()
tk.Entry(root, textvariable=user_var, font=entry_font, width=25).grid(row=0, column=1, pady=10, padx=5)
tk.Button(root, text="Select/Create User", font=btn_font, command=select_user).grid(row=0, column=2, padx=5)

tk.Label(root, text="Weight (kg):", font=label_font, bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
weight_entry = tk.Entry(root, font=entry_font)
weight_entry.grid(row=1, column=1, padx=5, pady=10)

tk.Label(root, text="Height (cm):", font=label_font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
height_entry = tk.Entry(root, font=entry_font)
height_entry.grid(row=2, column=1, padx=5, pady=10)

tk.Button(root, text="Calculate BMI", font=btn_font, bg="#0078D7", fg="white", command=calculate_bmi).grid(row=3, column=1, pady=15)

result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"), bg="#f0f0f0")
result_label.grid(row=4, column=1)

tk.Button(root, text="View History", font=btn_font, command=view_history).grid(row=5, column=0, pady=15)
tk.Button(root, text="Show BMI Graph", font=btn_font, command=show_graph).grid(row=5, column=2, pady=15)

if __name__ == "__main__":
    print("Starting app...")
    root.mainloop()
