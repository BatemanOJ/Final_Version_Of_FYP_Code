import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter GUI Comparison")
root.geometry("1000x700")

# Helper function to add labeled sliders
def create_slider(frame, text, from_, to_, row, resolution=1):
    label = tk.Label(frame, text=text, font=("Arial", 10))
    label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    slider = tk.Scale(frame, from_=from_, to=to_, orient="horizontal", resolution=resolution, length=300)
    slider.grid(row=row, column=1, padx=10, pady=5)
    return slider

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Create sliders (mirroring customtkinter GUI ones)
sliders = [
    ("Energy (Wh)", 0, 150000),
    ("Pack Mass (kg)", 0, 400),
    ("Max Voltage (V)", 0, 600),
    ("Min Voltage (V)", 0, 600),
    ("Discharging Power (W)", 0, 300000),
    ("Charging Power (W)", 0, 300000),
    ("Pack Volume (m³)", 0, 1, 0.01),
    ("EV Mass (kg)", 0, 3000),
    ("EV Drag Coefficient", 0.1, 1.0, 0.01),
    ("EV Frontal Area (m²)", 0, 4, 0.1),
    ("EV Rolling Resistance (N)", 0.001, 0.03, 0.001),
]

for idx, (label, min_val, max_val, *res) in enumerate(sliders):
    create_slider(main_frame, label, min_val, max_val, idx, resolution=res[0] if res else 1)

# Buttons (mirroring typical actions)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Calculate", width=20).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Export to Excel", width=20).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Plot Graph", width=20).grid(row=0, column=2, padx=10, pady=5)
tk.Button(button_frame, text="Reset Inputs", width=20).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Compare Batteries", width=20).grid(row=1, column=1, padx=10, pady=5)

root.mainloop()
