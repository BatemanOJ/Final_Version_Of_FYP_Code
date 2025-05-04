import customtkinter as ctk


from Main_Code_2 import Calculate_Possible_Combinations


# Create the main window
app = ctk.CTk()
app.title("Engineering Tool")
app.geometry("750x700")

# Default input values (Nissan Leaf)
defaults = {
    "Range": 170,
    "Total Energy": 28000,
    "Pack Mass": 315,
    "Max Voltage": 400,
    "Min Voltage": 240,
    "Discharging Power": 90000,
    "Charging Power": 50000
}

# Global references for input fields and sliders
inputs = {}
sliders = {}
labels = {}

# Create a label to display results
result_label = ctk.CTkLabel(app, text="")
result_label.grid(row=15, column=1, columnspan=2, pady=10)

# Error Label
error_label = ctk.CTkLabel(app, text="", text_color="red")
error_label.grid(row=16, column=1, columnspan=2, pady=10)

# Helper function to handle slider and input box syncing
def update_value(key, value):
    try:
        value = float(value)
        sliders[key].set(value)
        labels[key].configure(text=f"{value:.0f}")
        error_label.configure(text="")
    except ValueError:
        error_label.configure(text=f"Invalid value for {key}")

def sync_slider(key, value):
    value = float(value)
    inputs[key].delete(0, 'end')
    inputs[key].insert(0, f"{value:.0f}")
    labels[key].configure(text=f"{value:.0f}")

# Function to calculate based on inputs
def calculate():
    try:
        values = {key: float(inputs[key].get()) for key in defaults}
        output_range, fast_charging_time, battery_numbers, battery_data = Calculate_Possible_Combinations(
            values["Total Energy"], values["Discharging Power"], values["Max Voltage"],
            values["Min Voltage"], values["Pack Mass"], values["Charging Power"]
        )

        result_label.configure(
            text=f"Range: {output_range:.2f} km\n"
                 f"Minimum charging time: {fast_charging_time:.2f} mins"
        )
        error_label.configure(text="")
    except ValueError as e:
        error_label.configure(text="Invalid input. Please enter valid numbers.")

# Create Input + Slider + Label for each parameter
def create_input_row(name, row, from_, to_, step):
    inputs[name] = ctk.CTkEntry(app, placeholder_text=name, width=160, height=28)
    inputs[name].grid(row=row, column=1, padx=10, pady=5)
    inputs[name].insert(0, f"{defaults[name]}")
    
    sliders[name] = ctk.CTkSlider(app, from_=from_, to=to_, number_of_steps=step,
                                  command=lambda value, n=name: sync_slider(n, value))
    sliders[name].grid(row=row, column=2, padx=10, pady=5)
    sliders[name].set(defaults[name])
    
    labels[name] = ctk.CTkLabel(app, text=f"{defaults[name]}")
    labels[name].grid(row=row + 1, column=2)

    inputs[name].bind("<FocusOut>", lambda event, n=name: update_value(n, inputs[n].get()))

# Create rows for each parameter
create_input_row("Range", 1, 0, 1000, 200)
create_input_row("Total Energy", 3, 0, 150000, 150)
create_input_row("Pack Mass", 5, 0, 1000, 200)
create_input_row("Max Voltage", 7, 0, 1000, 200)
create_input_row("Min Voltage", 9, 0, 600, 120)
create_input_row("Discharging Power", 11, 0, 500000, 500)
create_input_row("Charging Power", 13, 0, 500000, 500)

# Create Calculate Button
calculate_button = ctk.CTkButton(app, text="Calculate", command=calculate)
calculate_button.grid(row=14, column=1, columnspan=2, pady=10)

# Start GUI loop
app.mainloop()
