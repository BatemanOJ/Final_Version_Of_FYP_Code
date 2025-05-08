
# Calcultes how long each battery will take to fast charge and regular charge from 10-80%

def Charging_times(battery_data_series_parallel, battery_1, battery_2):

    # print(f"Charging times: {successful_combinations[0]}")

    if battery_data_series_parallel[3] == 0:

        battery_1_capacity = battery_1[14] * battery_data_series_parallel[1]

        battery_1_voltage_max = battery_1[15] * battery_data_series_parallel[0]

        battery_1_max_charging_current = battery_1[23] * battery_data_series_parallel[1]

        battery_1_std_charging_current = battery_1[24]

        battery_1_min_time = 60 * ((battery_1_capacity * 0.8) - (battery_1_capacity * 0.1)) /battery_1_max_charging_current
        min_total_time = battery_1_min_time

        battery_1_max_charger_power = battery_1_max_charging_current * battery_1_voltage_max
        max_total_power = battery_1_max_charger_power

        battery_1_energy = battery_1[14] * battery_data_series_parallel[1] * battery_1[16] * battery_data_series_parallel[0]

        battery_1_min_time_from_energy = 60 * (((battery_1_energy * 0.8) - (battery_1_energy * 0.1)) /(battery_1_max_charger_power))
        min_total_time = battery_1_min_time_from_energy

        battery_1_std_time = ((battery_1_capacity * 0.8) - (battery_1_capacity * 0.1)) /battery_1_std_charging_current
        std_total_time = battery_1_std_time

        
    
    else: 

        battery_1_capacity = battery_1[14] * battery_data_series_parallel[1]
        battery_2_capacity = battery_2[14] * battery_data_series_parallel[3]

        battery_1_energy = battery_1[14] * battery_data_series_parallel[1] * battery_1[16] * battery_data_series_parallel[0]
        battery_2_energy = battery_2[14] * battery_data_series_parallel[3] * battery_2[16] * battery_data_series_parallel[2]
        total_energy = battery_1_energy + battery_2_energy

        battery_1_voltage_max = battery_1[15] * battery_data_series_parallel[0]
        battery_2_voltage_max = battery_2[15] * battery_data_series_parallel[2]

        battery_1_max_charging_current = battery_1[23] * battery_data_series_parallel[1]
        battery_2_max_charging_current = battery_2[23] * battery_data_series_parallel[3]

        battery_1_std_charging_current = battery_1[24]
        battery_2_std_charging_current = battery_2[24]

        battery_1_max_charger_power = battery_1_max_charging_current * battery_1_voltage_max
        battery_2_max_charger_power = battery_2_max_charging_current * battery_2_voltage_max
        max_total_power = battery_1_max_charger_power + battery_2_max_charger_power 

        if max_total_power < 480000:

            battery_1_min_time_from_energy = 60 * (((battery_1_energy * 0.8) - (battery_1_energy * 0.1)) /(battery_1_max_charger_power))
            battery_2_min_time_from_energy = 60 * (((battery_2_energy * 0.8) - (battery_2_energy * 0.1)) /(battery_2_max_charger_power))
            min_total_time = max(battery_1_min_time_from_energy, battery_2_min_time_from_energy)
        
        else:
            battery_1_min_time_from_energy_option_1 = 60 * (((battery_1_energy * 0.8) - (battery_1_energy * 0.1)) /(battery_1_max_charger_power))
            battery_2_min_time_from_energy_option_1 = 60 * (((battery_2_energy * 0.8) - (battery_2_energy * 0.1)) /(480000-battery_1_max_charger_power))

            battery_1_min_time_from_energy_option_2 = 60 * (((battery_1_energy * 0.8) - (battery_1_energy * 0.1)) /(480000-battery_2_max_charger_power))
            battery_2_min_time_from_energy_option_2 = 60 * (((battery_2_energy * 0.8) - (battery_2_energy * 0.1)) /(battery_2_max_charger_power))

            dont_want = max(battery_1_min_time_from_energy_option_1, battery_2_min_time_from_energy_option_1, battery_1_min_time_from_energy_option_2, battery_2_min_time_from_energy_option_2)
            if dont_want == battery_1_min_time_from_energy_option_1 or dont_want == battery_2_min_time_from_energy_option_1:
                min_total_time = max(battery_1_min_time_from_energy_option_2, battery_2_min_time_from_energy_option_2)
            else:
                min_total_time = max(battery_1_min_time_from_energy_option_1, battery_2_min_time_from_energy_option_1)

        # battery_1_min_time = 60 * ((battery_1_capacity * 0.8) - (battery_1_capacity * 0.1)) /battery_1_max_charging_current
        # battery_2_min_time = 60 * ((battery_2_capacity * 0.8) - (battery_2_capacity * 0.1)) /battery_2_max_charging_current
        # min_total_time = max(battery_1_min_time, battery_2_min_time)

        

        battery_1_std_time = ((battery_1_capacity * 0.8) - (battery_1_capacity * 0.1)) /battery_1_std_charging_current
        battery_2_std_time = ((battery_2_capacity * 0.8) - (battery_2_capacity * 0.1)) /battery_2_std_charging_current
        std_total_time = max(battery_1_std_time, battery_2_std_time)

        

    # print(f"Min charging times (mins): {battery_1_min_time, battery_2_min_time}, Min total time: {min_total_time}")
    # print(f"Standard charging times (hours): {battery_1_std_time, battery_2_std_time}, Standard total time: {std_total_time}")
    # print(f"Max charging power: {battery_1_max_charger_power, battery_2_max_charger_power}, Total power: {max_total_power}")
    


    return min_total_time, std_total_time, max_total_power