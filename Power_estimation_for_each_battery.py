

def Power_Estimation_for_Each_Battery(battery_data_series_parallel, battery_1, battery_2):

    power_1 = battery_data_series_parallel[0] * battery_data_series_parallel[1] * battery_1[16] * battery_1[19]
    power_2 = battery_data_series_parallel[2] * battery_data_series_parallel[3] * battery_2[16] * battery_2[19]

    return power_1, power_2