import pandas as pd
import numpy as np
import time

# from Two_Chem_Efficient_Battery_Mass_Not_Pack import Two_Chem_Efficient_Battery_Mass_Not_Pack
from Test_Two_Chem_Efficient_Battery_Mass_Not_Pack import Two_Chem_Efficient_Battery_Mass_Not_Pack
from Two_Chemistries import Two_Chemistries
from Two_Chem_Efficient import Two_Chem_Efficient
from Check_battery_index_order import Check_Battery_Order
from One_Chem_Comparison import One_Chem_Comparison

from Find_Battery_Combinations import Find_One_Batttery_Options



battery_1_index = 1
battery_2_index = 2

# for i in range(1, 388):
#     battery_{i}_index = Get_Battery_Data_Row(i)

# battery_data = {f"battery_{i}_index": Get_Battery_Data_Row(i).tolist() for i in range(1, 388)}
print("Started")
battery_data = {}

battery_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="RAW DATA")

i = 1
battery_data = {f"battery_{i}_index": battery_database.iloc[i].tolist() for i in range(333)}  # Adjusted for 333 rows

print("Battery Data Imported")

#############################################################

# Checks using battery mass not pack mass

multi_bat_success = 0
count_successful_combinations = 0
successful_combinations = []

start_time = time.time()

req_energy = 35000
req_discharging_power = 100000
req_max_V = 400
req_min_V = 240
req_max_mass_battery = 200
req_charging_power = 75000

tests = 0
fails = 0
tests_out = 0
fails_out = 0

while multi_bat_success == 0:

    Check_battery_1_order = battery_data[f"battery_{battery_1_index}_index"][1] 

    print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

    # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
    multi_bat_success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, energy, discharging_power, mass, charging_power, tests, fails = \
    Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"],\
                                             req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, tests, fails)
    
    tests_out += tests
    fails_out += fails

    if multi_bat_success == 1:
        # print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")
        
        # Check the battery indexes are the right way round
        check_battery_order = Check_Battery_Order (battery_data, battery_1_index, battery_2_index, battery_1_series, battery_1_parallel, \
                                                   battery_2_series, battery_2_parallel, energy)
        
        # print(f"Check Battery Order: {check_battery_order}")

        # successful_combinations.append([
        #     battery_1_index, battery_1_series, battery_1_parallel, 
        #     battery_2_index, battery_2_series, battery_2_parallel, 
        #     energy, discharging_power, mass, charging_power
        # ])

        # print(successful_combinations)

        if check_battery_order == 0:
            battery_hold_index = battery_1_index
            battery_1_index_switched = battery_2_index
            battery_2_index_switched = battery_hold_index
        elif check_battery_order == 1:
            battery_1_index_switched = battery_1_index
            battery_2_index_switched = battery_2_index

        successful_combinations.append([
            battery_1_index_switched, battery_1_series, battery_1_parallel, 
            battery_2_index_switched, battery_2_series, battery_2_parallel, 
            energy, discharging_power, mass, charging_power
        ])
        multi_bat_success = 0
        count_successful_combinations += 1

        # print(successful_combinations)

    if battery_1_index == 1 and battery_2_index == 378:
        break
    elif battery_2_index == 378:
        battery_1_index += 1
        battery_2_index = battery_1_index + 1
    else:
        battery_2_index += 1
      

    # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

# successful_combinations_store = [battery_1_index(1), battery_1_series(2), battery_1_parallel(3),
                                # battery_2_index(4), battery_2_series(5), battery_2_parallel(6),
                                # energy(7), discharging_power(8), mass(9), charging_power(10)]

end_time = time.time()  # End timer

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
        
print(count_successful_combinations)

if successful_combinations:
    max_energy_row = max(successful_combinations, key=lambda x: x[7])
    print(max_energy_row)

print(f"Tests: {tests_out}, Fails: {fails_out}")

#############################################################


# single_bat_success = 0
# count_successful_batteries = 0
# successful_batteries = []

# # # # Rivian R1T
# # # req_energy = 135000
# # # req_discharging_power = 511000
# # # req_max_V = 550
# # # req_min_V = 210
# # # req_max_mass_battery = 540
# # # req_charging_power = 210000

# # Nissan Leaf
# req_energy = 27700
# req_discharging_power = 90000
# req_max_V = 398
# req_min_V = 240
# req_max_mass_battery = 315
# req_charging_power = 50000


# successful_batteries, count_successful_batteries = Find_One_Batttery_Options(battery_data, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power)
    
# print(count_successful_batteries)
# print(f"Successful combos: {successful_batteries}")

# if successful_batteries:
#     max_energy_row_single_bat = max(successful_batteries, key=lambda x: x[3])
#     # print(max_energy_row_single_bat)



########################################################################################