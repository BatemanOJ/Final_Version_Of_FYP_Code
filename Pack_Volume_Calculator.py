import math
from math import pi


def volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume):
    
    if battery_1[30] == 'not applicable':
        # print("Battery 1 is a prismatic cell")
        battery_1_volume = (((battery_1[27] * battery_1[28] * battery_1[29])/1000000000) / battery_1[41])*100
        # print(f"1 length: {battery_1[27]}, width: {battery_1[29]}, height: {battery_1[28]}")
    else:
        battery_1_volume = (((pi * (battery_1[30]/2)**2 * battery_1[28])/1000000000) / battery_1[41])*100
        # print(f"1 diameter: {battery_1[30]}, height: {battery_1[28]}")
    
    if battery_2[30] == 'not applicable':
        # print("Battery 2 is a prismatic cell")
        battery_2_volume = (((battery_2[27] * battery_2[28] * battery_2[29])/1000000000) / battery_1[41])*100
        # print(f"2 length: {battery_2[27]}, width: {battery_2[29]}, height: {battery_2[28]}")
    else:
        battery_2_volume = (((pi * (battery_2[30]/2)**2 * battery_2[28])/1000000000) / battery_1[41])*100
        # print(f"2 diameter: {battery_2[30]}, height: {battery_2[28]}")

    total_volume = ((battery_1_volume * no_battery_1_series * no_battery_1_parallel) + (battery_2_volume * no_battery_2_series * no_battery_2_parallel))
    # total_volume_adjusted = total_volume/0.4

    if total_volume > max_volume:
        # print(f"Total volume: {total_volume_adjusted} L, exceeds maximum volume of {max_volume} L")
        volume_check = 0
    else:
        # print(f"Total volume: {total_volume_adjusted} L, within maximum volume of {max_volume} L")
        volume_check = 1

    return total_volume, volume_check

def volume_calculator_one_battery(battery_1, no_battery_1_series, no_battery_1_parallel, max_volume):
        
        if battery_1[30] == 'not applicable':
            # print("Battery 1 is a prismatic cell")
            battery_1_volume = (((battery_1[27] * battery_1[28] * battery_1[29])/1000000000) / battery_1[41])*100
            # print(f"1 length: {battery_1[27]}, width: {battery_1[29]}, height: {battery_1[28]}")
        else:
            battery_1_volume = (((pi * (battery_1[30]/2)**2 * battery_1[28])/1000000000) / battery_1[41])*100
            # print(f"1 diameter: {battery_1[30]}, height: {battery_1[28]}")
    
        total_volume = (battery_1_volume * no_battery_1_series * no_battery_1_parallel)
        # total_volume_adjusted = total_volume/0.4
    
        if total_volume > max_volume:
            # print(f"Total volume: {total_volume_adjusted} L, exceeds maximum volume of {max_volume} L")
            volume_check = 0
        else:
            # print(f"Total volume: {total_volume_adjusted} L, within maximum volume of {max_volume} L")
            volume_check = 1
    
        return total_volume, volume_check