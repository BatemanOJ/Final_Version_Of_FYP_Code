import numpy as np
import math

from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1

def Series_Parallel_Config_EV(EV_number): #, no_cells_series, no_cells_parallel, max_cells_parallel, peak_cell_current, min_cell_voltage, \
                           #peak_discharge_power, max_cells_series, min_cells_series, series_values, parallel_values):


    # Data retrieved from the excel sheet containing EV database
    EV_required_capacity = Get_Data_EVs(7, EV_number)
    cell_energy_capacity = Get_Data_EVs(33, EV_number)

    min_pack_voltage = Get_Data_EVs(21, EV_number)
    max_pack_voltage = Get_Data_EVs(20, EV_number)

    min_cell_voltage = Get_Data_EVs(31, EV_number)
    max_cell_voltage = Get_Data_EVs(29, EV_number)
    voltage_for_peak_power = Get_Data_EVs(41, EV_number)

    peak_discharge_power = Get_Data_EVs(12, EV_number) #190512

    peak_cell_current = Get_Data_EVs(34, EV_number)
    nominal_pack_capacity = Get_Data_EVs(19, EV_number)
    cell_capacity_Ah = Get_Data_EVs(32, EV_number)

    # Calculate the minimum number of cells required for the EV capacity requirement
    min_cells = EV_required_capacity/cell_energy_capacity

    # Calculate the min and max number of cells in series for EV voltage requirements
    min_cells_series = math.ceil(min_pack_voltage/min_cell_voltage)
    max_cells_series = math.ceil(max_pack_voltage/max_cell_voltage)

    # Calculate the min and max number of cells in parallel for EV requirements
    min_cells_parallel = math.ceil(min_cells/max_cells_series)
    max_cells_parallel = math.ceil(nominal_pack_capacity/cell_capacity_Ah)
    # print(max_cells_parallel, min_cells_parallel)

    no_cells_series = min_cells_series
    no_cells_parallel = min_cells_parallel

    series_values = []
    parallel_values = []

   
    # Finds the series-parallel configuration that meets the peak power, 
    # max and min voltage and current requirements of the EV
    while no_cells_parallel <= max_cells_parallel:
        # print(peak_cell_current * no_cells_parallel * voltage_for_peak_power * no_cells_series, peak_discharge_power)
        if (peak_cell_current * no_cells_parallel * voltage_for_peak_power * no_cells_series) < peak_discharge_power:
            
            result = peak_cell_current * no_cells_parallel * voltage_for_peak_power * no_cells_series
            # print(peak_discharge_power, result, no_cells_parallel, no_cells_series)

            if peak_discharge_power - result < peak_cell_current * no_cells_parallel *\
            ((voltage_for_peak_power * max_cells_series) - (voltage_for_peak_power * min_cells_series)):

                if no_cells_series < max_cells_series:
                    no_cells_series += 1

            else:
                if no_cells_parallel < max_cells_parallel:
                    no_cells_parallel += 1

                else:
                    print("No combination found")
                    break
            
        else:
            
            series_values.append(no_cells_series)
            parallel_values.append(no_cells_parallel)
            
            no_cells_series = min_cells_series
            no_cells_parallel += 1

    i = 0
    # Checks if the series-paralle config found above meets the EVs energy capcity requirements
    while i < (len(series_values)):
        calculated_pack_capacity = series_values[i] * parallel_values[i] * cell_energy_capacity

        if calculated_pack_capacity < EV_required_capacity:
            series_values[i] += 1

            if series_values[i] == max_cells_series:
            
                series_values.remove(i)
                parallel_values.remove(i)
        
        else:
            i += 1

    i = 0
    # Finds the minimum number of cells that meet the requirements of the EV, 
    # i.e. if 106s 1p and 106s 2p meet requirements it selects 106s 1p
    while (len(series_values)) > 1:
        # print(series_values, parallel_values)

        if series_values[i] * parallel_values[i] < series_values[i+1] * parallel_values[i+1]:
            del series_values[i+1]
            del parallel_values[i+1]
        elif series_values[i] * parallel_values[i] > series_values[i+1] * parallel_values[i+1]:
            del series_values[i]
            del parallel_values[i]

    calculated_pack_capacity = series_values[i] * parallel_values[i] * cell_energy_capacity
    
    return series_values, parallel_values, max_cells_series, calculated_pack_capacity