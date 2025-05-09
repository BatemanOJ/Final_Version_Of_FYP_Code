import customtkinter as ctk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_scatter(successful_combinations_1_bat, successful_combinations_2_bat):
    
    if successful_combinations_1_bat != 0 or successful_combinations_2_bat != 0:
        
        plot_window = ctk.CTkToplevel()
        plot_window.title("Range vs. Minimum Charging Time")
        plot_window.geometry("750x600")

        # Create a new figure
        fig, ax = plt.subplots()

        # Ensure the figure is closed properly when the window is closed
        def on_close():
            plt.close(fig)  # Close the Matplotlib figure
            plot_window.destroy()  # Destroy the window

        plot_window.protocol("WM_DELETE_WINDOW", on_close)  # Handle close event

        # print(f"successful_combinations_1_bat: {successful_combinations_1_bat}, successful_combinations_2_bat: {successful_combinations_2_bat}")

        

        if successful_combinations_2_bat != 0:
            range_data_bat_2 = [row[10] for row in successful_combinations_2_bat]
            charging_data_bat_2 = [row[11] for row in successful_combinations_2_bat]

            charging_speed_bat_2 = []
            for i in range(len(charging_data_bat_2)):
                charging_speed = (range_data_bat_2[i]*0.8 - range_data_bat_2[i]*0.1) / charging_data_bat_2[i]
                charging_speed_bat_2.append(charging_speed)


            ax.scatter(range_data_bat_2, charging_speed_bat_2, color='blue', label='2 Battery Options')
            range_data_all = range_data_bat_2
            charging_data_all = charging_data_bat_2
            charging_speed_data_all = charging_speed_bat_2


        if successful_combinations_1_bat != 0:
            range_data_bat_1 = [row[10] for row in successful_combinations_1_bat]
            charging_data_bat_1 = [row[11] for row in successful_combinations_1_bat]
            charging_speed_bat_1 = []
            for i in range(len(charging_data_bat_1)):
                charging_speed = (range_data_bat_1[i]*0.8 - range_data_bat_1[i]*0.1) / charging_data_bat_1[i]
                charging_speed_bat_1.append(charging_speed)

            ax.scatter(range_data_bat_1, charging_speed_bat_1, color='red', label='1 Battery Options')
            range_data_all.extend(range_data_bat_1)
            charging_data_all.extend(charging_data_bat_1)
            charging_speed_data_all.extend(charging_speed_bat_1)
        # print(len(range_data_bat_1), len(charging_data_bat_1))
        # print(len(range_data_bat_2), len(charging_data_bat_2))
        
        ax.set_title("Range vs. Minimum Charging Time")
        ax.set_xlabel("Range (km)")
        ax.set_ylabel("Charging Speed (km/min)")
        ax.legend()

        # Embed the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=plot_window)  # Embed in the app
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10)

        # Click label
        click_label = ctk.CTkLabel(plot_window, text="Click on a point to see details")
        click_label.pack(pady=10)

        canvas.mpl_connect("button_press_event", lambda event: on_click(event, ax, range_data_all, charging_speed_data_all, click_label))   # Click on a point
        # canvas.mpl_connect("motion_notify_event", lambda event: on_hover(event, ax, range_data_all, charging_data_all, hover_label))  # Hover over a point  

    else:
        print("No data to plot")


def on_click(event, ax, range_data_all, charging_speed_data_all, click_label: ctk.CTkLabel):
    if event.inaxes == ax:
        # Find closest point
        distances = np.sqrt((range_data_all - event.xdata) ** 2 + (charging_speed_data_all - event.ydata) ** 2)
        index = np.argmin(distances)
        print(f"Index: {index}\nRange: {range_data_all[index]:.1f}, Charging Time: {charging_speed_data_all[index]:.1f}\nRange clicked: {event.xdata:.1f}, Charging Time clicked: {event.ydata:.1f}")
        click_label.configure(text=f"Range (km): {range_data_all[index]:.1f}\nCharging Speed (km/min): {charging_speed_data_all[index]:.1f}")



# def on_hover(event, ax, range_data_all, charging_data_all, hover_label: ctk.CTkLabel):
#     if event.inaxes == ax:
#         distances = np.sqrt((range_data_all - event.xdata) ** 2 + (charging_data_all - event.ydata) ** 2)
#         index = np.argmin(distances)
#         if distances[index] < 5:  # Adjust sensitivity as needed
#             hover_label.configure(text=f"Range: {range_data_all[index]:.1f}\nCharging Time: {charging_data_all[index]:.1f}")
#         else:
#             hover_label.configure(text="")


def plot_scatter_current_options(successful_combinations_1_bat, successful_combinations_2_bat, \
                                 desired_range, desired_km_per_min, desired_max_discharging_power, desired_max_mass):
    
    desired_values = [desired_range, desired_km_per_min]
    
    matching_rows_1_bat = [row for row in successful_combinations_1_bat if row[10] >= desired_values[0] and (0.8*row[10] - 0.1*row[10])/row[11] >= desired_values[1]\
                         and row[7]/1000 >= desired_max_discharging_power and row[8] <= desired_max_mass]
    
    matching_rows_2_bat = [row for row in successful_combinations_2_bat if row[10] >= desired_values[0] and (0.8*row[10] - 0.1*row[10])/row[11] >= desired_values[1]\
                         and row[7]/1000 >= desired_max_discharging_power and row[8] <= desired_max_mass]

    if matching_rows_1_bat != 0 or matching_rows_2_bat != 0:
        
        plot_window = ctk.CTkToplevel()
        plot_window.title("Range vs. Minimum Charging Time")
        plot_window.geometry("750x600")

        # Create a new figure
        fig, ax = plt.subplots()

        # Ensure the figure is closed properly when the window is closed
        def on_close():
            plt.close(fig)  # Close the Matplotlib figure
            plot_window.destroy()  # Destroy the window

        plot_window.protocol("WM_DELETE_WINDOW", on_close)  # Handle close event

        # print(f"successful_combinations_1_bat: {successful_combinations_1_bat}, successful_combinations_2_bat: {successful_combinations_2_bat}")

        
        if matching_rows_2_bat != 0:
            range_data_bat_2 = [row[10] for row in matching_rows_2_bat]
            charging_data_bat_2 = [row[11] for row in matching_rows_2_bat]

            charging_speed_bat_2 = []
            for i in range(len(charging_data_bat_2)):
                charging_speed = (range_data_bat_2[i]*0.8 - range_data_bat_2[i]*0.1) / charging_data_bat_2[i]
                charging_speed_bat_2.append(charging_speed)


            ax.scatter(range_data_bat_2, charging_speed_bat_2, color='blue', label='HESS Options')
            range_data_all = range_data_bat_2
            charging_data_all = charging_data_bat_2
            charging_speed_data_all = charging_speed_bat_2


        if matching_rows_1_bat != 0:
            range_data_bat_1 = [row[10] for row in matching_rows_1_bat]
            charging_data_bat_1 = [row[11] for row in matching_rows_1_bat]
            charging_speed_bat_1 = []
            for i in range(len(charging_data_bat_1)):
                charging_speed = (range_data_bat_1[i]*0.8 - range_data_bat_1[i]*0.1) / charging_data_bat_1[i]
                charging_speed_bat_1.append(charging_speed)

            ax.scatter(range_data_bat_1, charging_speed_bat_1, color='red', label='SESS Options')
            range_data_all.extend(range_data_bat_1)
            charging_data_all.extend(charging_data_bat_1)
            charging_speed_data_all.extend(charging_speed_bat_1)
        # print(len(range_data_bat_1), len(charging_data_bat_1))
        # print(len(range_data_bat_2), len(charging_data_bat_2))
        
        ax.set_title("Range vs. Minimum Charging Time")
        ax.set_xlabel("Range (km)")
        ax.set_ylabel("Carging Speed (km/min)")
        ax.legend()

        # Embed the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=plot_window)  # Embed in the app
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10)

        # Click label
        click_label = ctk.CTkLabel(plot_window, text="Click on a point to see details")
        click_label.pack(pady=10)

        canvas.mpl_connect("button_press_event", lambda event: on_click(event, ax, range_data_all, charging_speed_data_all, click_label))   # Click on a point
        # canvas.mpl_connect("motion_notify_event", lambda event: on_hover(event, ax, range_data_all, charging_data_all, hover_label))  # Hover over a point  

    else:
        print("No data to plot")