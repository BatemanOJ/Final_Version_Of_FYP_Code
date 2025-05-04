import math
import numpy as np




def check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, original_max_volume, max_volume, required_power, req_charging_power):

    battery_1_peak_power = battery_1[16] * battery_1[19]
    battery_2_peak_power = battery_2[16] * battery_2[19]

    battery_1_peak_charge_power = battery_1[16] * battery_1[23]
    battery_2_peak_charge_power = battery_2[16] * battery_2[23]

    peak_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_power
    
    peak_charge_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_charge_power + \
                                  no_battery_2_series * no_battery_2_parallel * battery_2_peak_charge_power
    
    # if battery_1[27] == 275:
    #     print(f"Maximum mass: {original_max_mass}, peak power generated: {peak_power_generated}, peak charge power generated: {peak_charge_power_generated}")
    
    if peak_charge_power_generated < peak_power_generated:
        if peak_power_generated < required_power:
            return original_max_mass, original_max_volume
        
        else: 
            max_mass = original_max_mass - (((peak_power_generated)/62000))
            # print(desired_EV_characteristics[2])
            max_volume = original_max_volume - (((peak_power_generated)/143000000))
            return max_mass, max_volume
    else:
        if peak_charge_power_generated < required_power:
            return original_max_mass, original_max_volume
        
        else: 
            max_mass = original_max_mass - (((peak_charge_power_generated)/62000))
            # print(desired_EV_characteristics[2])
            max_volume = original_max_volume - (((peak_charge_power_generated)/143000000))
            return max_mass, max_volume
