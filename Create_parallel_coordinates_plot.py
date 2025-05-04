import customtkinter as ctk
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_parallel_coordinates_plot(successful_combinations, has_calculate_been_pressed):
    # Generate some sample data
    if has_calculate_been_pressed == 0:
        print("No data to plot. Please run the calculation first.")
    elif has_calculate_been_pressed == 1:
        
        transposed_data = [list(t) for t in zip(*successful_combinations)]
        # print(transposed_data[10])
        power_in_kw = []

        for i in range(0, len(successful_combinations)):
            power_in_kw.append(successful_combinations[i][7] / 1000) # Convert to kW

        list_km_per_min = []
        for i in range(0, len(successful_combinations)):
            km_per_min = (0.8*successful_combinations[i][10] - 0.1*successful_combinations[i][10])/successful_combinations[i][11]
            list_km_per_min.append(km_per_min)

        Range = np.array(transposed_data[10])
        km_per_min = np.array(list_km_per_min)
        Max_discharging_power = np.array(power_in_kw) # Convert to kW
        Min_pack_mass = np.array(transposed_data[8])

        # print(f"km_per_min: {km_per_min}")

        df = pd.DataFrame({
            'Range (km)': Range,
            'Charging speed (km/min)': km_per_min, 
            'Max discharging power (kW)': Max_discharging_power,
            'Min pack mass (kg)': Min_pack_mass
        })

        df_test = pd.DataFrame({
            'A': np.random.rand(100),
            'B': np.random.rand(100),
            'C': np.random.rand(100),
            'D': np.random.rand(100),
            'E': np.random.rand(100)
        })

        fig = px.parallel_coordinates(df, 
                                dimensions=['Min pack mass (kg)', 'Range (km)', 'Charging speed (km/min)', 'Max discharging power (kW)'],
                                color='Range (km)',
                                color_continuous_scale=px.colors.diverging.Tealrose)
        fig.show()
        fig_test = px.parallel_coordinates(df_test, 
                                dimensions=['A', 'B', 'C', 'D', 'E'],
                                color='A',
                                color_continuous_scale=px.colors.diverging.Tealrose)
        # fig_test.show()

# create_parallel_coordinates_plot()