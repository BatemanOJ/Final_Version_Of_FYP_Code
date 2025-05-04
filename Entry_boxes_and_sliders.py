import customtkinter as ctk

# from GUI_Test import update_range_label, update_total_energy_label, \
#                      update_Pack_mass_label, update_Max_V_label, \
#                      update_Min_V_label, update_Discharging_power_label, \
#                      update_Charging_power_label

def Make_Entry_boxes_and_sliders(app, default_name, default_input, row, column, max, middle, min, num_steps, name):

    # Peak Charging Power
    Charging_power = ctk.CTkEntry(app, placeholder_text=f"{name}", width=175, height=28)
    Charging_power.grid(row= row, column= column-1, padx=10, pady=10)

    # Charging slider label
    Charging_power_min_label = ctk.CTkLabel(app, text=f"\n\n\n      {min}", font=("Helvetica", 10))
    Charging_power_min_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_label = ctk.CTkLabel(app, text=f"\n\n\n{middle}", font=("Helvetica", 10))
    Charging_power_mid_label.grid(row=row, column=column)
    Charging_power_max_label = ctk.CTkLabel(app, text=f"\n\n\n{max}      ", font=("Helvetica", 10))
    Charging_power_max_label.grid(row=row, column=column, sticky="e")


    Charging_power_slider = ctk.CTkSlider(app, from_=min, to=max, number_of_steps=num_steps)
    Charging_power_slider.grid(row= row, column=column, padx=0, pady=0)
    Charging_power_slider.set(default_input)
    Charging_power_label = ctk.CTkLabel(app, text= f"{default_name}{default_input}")
    Charging_power_label.grid(row= row+1, column=column)

    Charging_power_min_dash_label = ctk.CTkLabel(app, text="       |", font=("Helvetica", 7))
    Charging_power_min_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
    Charging_power_mid_dash_label.grid(row=row, column=column)
    Charging_power_max_dash_label = ctk.CTkLabel(app, text="|       ", font=("Helvetica", 7))
    Charging_power_max_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="e")

    return Charging_power, Charging_power_slider, Charging_power_label

def Make_Sliders(app, default_name, default_input, row, column, max, middle, min, num_steps):

    # Charging slider label
    Charging_power_min_label = ctk.CTkLabel(app, text=f"\n\n\n      {min}", font=("Helvetica", 10))
    Charging_power_min_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_label = ctk.CTkLabel(app, text=f"\n\n\n{middle}", font=("Helvetica", 10))
    Charging_power_mid_label.grid(row=row, column=column)
    Charging_power_max_label = ctk.CTkLabel(app, text=f"\n\n\n{max}      ", font=("Helvetica", 10))
    Charging_power_max_label.grid(row=row, column=column, sticky="e")


    Charging_power_slider = ctk.CTkSlider(app, from_=min, to=max, number_of_steps=num_steps, state="disabled")
    Charging_power_slider.grid(row= row, column=column, padx=0, pady=0)
    Charging_power_slider.set(default_input)
    Charging_power_label = ctk.CTkLabel(app, text= f"{default_name}{default_input:.2f}")
    Charging_power_label.grid(row= row+1, column=column)

    Charging_power_min_dash_label = ctk.CTkLabel(app, text="       |", font=("Helvetica", 7))
    Charging_power_min_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
    Charging_power_mid_dash_label.grid(row=row, column=column)
    Charging_power_max_dash_label = ctk.CTkLabel(app, text="|       ", font=("Helvetica", 7))
    Charging_power_max_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="e")

    return Charging_power_slider, Charging_power_label

def Make_Sliders_1_sf(app, default_name, default_input, row, column, max, middle, min, num_steps):

    # Charging slider label
    Charging_power_min_label = ctk.CTkLabel(app, text=f"\n\n\n      {min}", font=("Helvetica", 10))
    Charging_power_min_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_label = ctk.CTkLabel(app, text=f"\n\n\n{middle}", font=("Helvetica", 10))
    Charging_power_mid_label.grid(row=row, column=column)
    Charging_power_max_label = ctk.CTkLabel(app, text=f"\n\n\n{max}      ", font=("Helvetica", 10))
    Charging_power_max_label.grid(row=row, column=column, sticky="e")


    Charging_power_slider = ctk.CTkSlider(app, from_=min, to=max, number_of_steps=num_steps, state="disabled")
    Charging_power_slider.grid(row= row, column=column, padx=0, pady=0)
    print(f"default_input: {default_input}")
    Charging_power_slider.set(1)
    Charging_power_label = ctk.CTkLabel(app, text= f"{default_name}{default_input:.1f}")
    Charging_power_label.grid(row= row+1, column=column)

    Charging_power_min_dash_label = ctk.CTkLabel(app, text="       |", font=("Helvetica", 7))
    Charging_power_min_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
    Charging_power_mid_dash_label.grid(row=row, column=column)
    Charging_power_max_dash_label = ctk.CTkLabel(app, text="|       ", font=("Helvetica", 7))
    Charging_power_max_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="e")

    return Charging_power_slider, Charging_power_label

def Make_Sliders_desired_values(app, default_name, default_input, row, column, max, middle, min, num_steps):

    # Charging slider label
    Charging_power_min_label = ctk.CTkLabel(app, text=f"\n\n\n      {min:.0f}", font=("Helvetica", 10))
    Charging_power_min_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_label = ctk.CTkLabel(app, text=f"\n\n\n{middle:.0f}", font=("Helvetica", 10))
    Charging_power_mid_label.grid(row=row, column=column)
    Charging_power_max_label = ctk.CTkLabel(app, text=f"\n\n\n{max:.0f}      ", font=("Helvetica", 10))
    Charging_power_max_label.grid(row=row, column=column, sticky="e")


    Charging_power_slider = ctk.CTkSlider(app, from_=min, to=max, number_of_steps=num_steps, state="disabled")
    Charging_power_slider.grid(row= row, column=column, padx=0, pady=0)
    Charging_power_slider.set(default_input)
    Charging_power_label = ctk.CTkLabel(app, text= f"{default_name}{default_input:.0f}")
    Charging_power_label.grid(row= row+1, column=column)

    Charging_power_min_dash_label = ctk.CTkLabel(app, text="       |", font=("Helvetica", 7))
    Charging_power_min_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="w")
    Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
    Charging_power_mid_dash_label.grid(row=row, column=column)
    Charging_power_max_dash_label = ctk.CTkLabel(app, text="|       ", font=("Helvetica", 7))
    Charging_power_max_dash_label.grid(row=row, column=column, padx=0, pady=0, sticky="e")

    return Charging_power_slider, Charging_power_label
    

def Charging_Power(app, input_charging_power):
    # Peak Charging Power
    Charging_power = ctk.CTkEntry(app, placeholder_text="Peak Charging Power", width=160, height=28)
    Charging_power.grid(row= 13, column= 1, padx=10, pady=10)

    # Charging slider label
    Charging_power_min_label = ctk.CTkLabel(app, text="\n\n\n      0", font=("Helvetica", 10))
    Charging_power_min_label.grid(row=13, column=2, padx=0, pady=0, sticky="w")
    Charging_power_mid_label = ctk.CTkLabel(app, text="\n\n\n150000", font=("Helvetica", 10))
    Charging_power_mid_label.grid(row=13, column=2)
    Charging_power_max_label = ctk.CTkLabel(app, text="\n\n\n300000", font=("Helvetica", 10))
    Charging_power_max_label.grid(row=13, column=2, sticky="e")


    Charging_power_slider = ctk.CTkSlider(app, from_=0, to=300000, number_of_steps=300)
    Charging_power_slider.grid(row= 13, column=2, padx=0, pady=0)
    Charging_power_slider.set(input_charging_power)
    # Charging_power_slider.configure(command=update_Charging_power_label)
    Charging_power_label = ctk.CTkLabel(app, text=input_charging_power)
    Charging_power_label.grid(row= 15, column=2)

    Charging_power_min_dash_label = ctk.CTkLabel(app, text="        |", font=("Helvetica", 7))
    Charging_power_min_dash_label.grid(row=13, column=2, padx=0, pady=0, sticky="w")
    Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
    Charging_power_mid_dash_label.grid(row=13, column=2)
    Charging_power_max_dash_label = ctk.CTkLabel(app, text="|        ", font=("Helvetica", 7))
    Charging_power_max_dash_label.grid(row=13, column=2, padx=0, pady=0, sticky="e")




# # Range
# EV_range = ctk.CTkEntry(app, placeholder_text="Range", width=160, height=28)
# EV_range.grid(row= 1, column= 1, padx=10, pady=10)
# EV_range_slider = ctk.CTkSlider(app, from_=0, to=1000, number_of_steps=2)
# EV_range_slider.grid(row= 1, column=2, padx=10, pady=10)
# EV_range_slider.set(input_range)
# # EV_range_slider.configure(command=update_range_label)
# EV_range_label = ctk.CTkLabel(app, text=input_range)
# EV_range_label.grid(row=2, column=2)

# Total Energy
# total_energy = ctk.CTkEntry(app, placeholder_text="Total Energy", width=160, height=28)
# total_energy.grid(row= 3, column= 1, padx=10, pady=10)
# total_energy_slider = ctk.CTkSlider(app, from_= 0, to=150000, number_of_steps=150)
# total_energy_slider.grid(row= 3, column=2, padx=10, pady=10)
# total_energy_slider.set(input_energy)
# total_energy_slider.configure(command=update_total_energy_label)
# total_energy_label = ctk.CTkLabel(app, text=input_energy)
# total_energy_label.grid(row= 4, column=2)

# Pack_mass = ctk.CTkEntry(app, placeholder_text="Pack Mass", width=160, height=28)
# Pack_mass.grid(row= 5, column= 1, padx=10, pady=10)
# Pack_mass_slider = ctk.CTkSlider(app, from_=0, to=1000, number_of_steps=200)
# Pack_mass_slider.grid(row= 5, column=2, padx=10, pady=10)
# Pack_mass_slider.set(input_max_mass_pack)
# Pack_mass_slider.configure(command=update_Pack_mass_label)
# Pack_mass_label = ctk.CTkLabel(app, text=input_max_mass_pack)
# Pack_mass_label.grid(row= 6, column=2)

# Max_V = ctk.CTkEntry(app, placeholder_text="Maximum Voltage", width=160, height=28)
# Max_V.grid(row= 7, column= 1, padx=10, pady=10)
# Max_V_slider = ctk.CTkSlider(app, from_=0, to=1000, number_of_steps=200)
# Max_V_slider.grid(row= 7, column=2, padx=10, pady=10)
# Max_V_slider.set(input_max_V)
# Max_V_slider.configure(command=update_Max_V_label)
# Max_V_label = ctk.CTkLabel(app, text=input_max_V)
# Max_V_label.grid(row= 8, column=2)

# Min_V = ctk.CTkEntry(app, placeholder_text="Minimum Voltage", width=160, height=28)
# Min_V.grid(row= 9, column= 1, padx=10, pady=10)
# Min_V_slider = ctk.CTkSlider(app, from_=0, to=600, number_of_steps=120)
# Min_V_slider.grid(row= 9, column=2, padx=10, pady=10)
# Min_V_slider.set(input_min_V)
# Min_V_slider.configure(command=update_Min_V_label)
# Min_V_label = ctk.CTkLabel(app, text=input_min_V)
# Min_V_label.grid(row= 10, column=2)

# Discharging_power = ctk.CTkEntry(app, placeholder_text="Peak Discharging Power", width=160, height=28)
# Discharging_power.grid(row= 11, column= 1, padx=10, pady=10)
# Discharging_power_slider = ctk.CTkSlider(app, from_=0, to=500000, number_of_steps=500)
# Discharging_power_slider.grid(row= 11, column=2, padx=10, pady=10)
# Discharging_power_slider.set(input_discharging_power)
# Discharging_power_slider.configure(command=update_Discharging_power_label)
# Discharging_power_label = ctk.CTkLabel(app, text=input_discharging_power)
# Discharging_power_label.grid(row= 12, column=2)

# # Peak Charging Power
# Charging_power = ctk.CTkEntry(app, placeholder_text="Peak Charging Power", width=160, height=28)
# Charging_power.grid(row= 13, column= 1, padx=10, pady=10)

# # Charging slider label
# Charging_power_min_label = ctk.CTkLabel(app, text="\n\n\n      0", font=("Helvetica", 10))
# Charging_power_min_label.grid(row=13, column=2, padx=0, pady=0, sticky="w")
# Charging_power_mid_label = ctk.CTkLabel(app, text="\n\n\n150000", font=("Helvetica", 10))
# Charging_power_mid_label.grid(row=13, column=2)
# Charging_power_max_label = ctk.CTkLabel(app, text="\n\n\n300000", font=("Helvetica", 10))
# Charging_power_max_label.grid(row=13, column=2, sticky="e")


# Charging_power_slider = ctk.CTkSlider(app, from_=0, to=300000, number_of_steps=300)
# Charging_power_slider.grid(row= 13, column=2, padx=0, pady=0)
# Charging_power_slider.set(input_charging_power)
# Charging_power_slider.configure(command=update_Charging_power_label)
# Charging_power_label = ctk.CTkLabel(app, text=input_charging_power)
# Charging_power_label.grid(row= 15, column=2)

# Charging_power_min_dash_label = ctk.CTkLabel(app, text="        |", font=("Helvetica", 7))
# Charging_power_min_dash_label.grid(row=13, column=2, padx=0, pady=0, sticky="w")
# Charging_power_mid_dash_label = ctk.CTkLabel(app, text="|", font=("Helvetica", 7))
# Charging_power_mid_dash_label.grid(row=13, column=2)
# Charging_power_max_dash_label = ctk.CTkLabel(app, text="|        ", font=("Helvetica", 7))
# Charging_power_max_dash_label.grid(row=13, column=2, padx=0, pady=0, sticky="e")
