import pandas as pd


# from Get_Data_From_Cell import Get_Data_Battery_Cell # row -3, column -2
# from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1
# from Series_parallel_configuration import Series_Parallel_Config_EV 
# from Range_Estimation import Range_Estimation_for_EVs
# from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array -2 on the row number
# from Two_Chemistries import Two_Chemistries
# from Two_Chem_Efficient import Two_Chem_Efficient
# from Two_Chem_Efficient_Battery_Mass_Not_Pack import Two_Chem_Efficient_Battery_Mass_Not_Pack
# from One_Chem_Comparison import One_Chem_Comparison
from Range_Estimation import Range_Estimation_for_Batteries
# from Check_battery_index_order import Check_Battery_Order
from Compare_Best_Combinations import Compare_Best_Combination
from Calculate_Charging_Time import Charging_times

from Find_Battery_Combinations import Find_One_Battery_Options, Find_Two_Battery_Options, Find_Two_Battery_Options_Test, Find_Two_Battery_Options_Test_with_removed




# success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, capacity, power, mass = \
#     Two_Chem_Efficient(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"], 135000, 511000, 459, 289, 540)
# print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")


#############################################################

# # Checks using pack mass not battery mass

# multi_bat_success = 0
# count_successful_combinations = 0
# successful_combinations = []

# start_time = time.time()

# while multi_bat_success == 0:

#     # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
#     multi_bat_success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, capacity, discharging_power, mass, charging_power = \
#     Two_Chem_Efficient(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"], 75000, 250000, 459, 289, 520, 160000)

#     if multi_bat_success == 1:
#         # print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")
        
#         successful_combinations.append([
#             battery_1_index, battery_1_series, battery_1_parallel, 
#             battery_2_index, battery_2_series, battery_2_parallel, 
#             capacity, discharging_power, mass, charging_power
#         ])
#         multi_bat_success = 0
#         count_successful_combinations += 1

#     if battery_2_index == 378 and battery_1_index == 377:
#         break
#     elif battery_2_index == 378:
#         battery_1_index += 1
#         battery_2_index = battery_1_index + 1
#     else:
#         battery_2_index += 1
      

#     # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

# # successful_combinations_store = [battery_1_index(1), battery_1_series(2), battery_1_parallel(3),
#                                 # battery_2_index(4), battery_2_series(5), battery_2_parallel(6),
#                                 # capacity(7), discharging_power(8), mass(9), charging_power(10)]

# end_time = time.time()  # End timer

# elapsed_time = end_time - start_time
# print(f"Elapsed time: {elapsed_time:.6f} seconds")
        
# print(count_successful_combinations)

# if successful_combinations:
#     max_capacity_row = max(successful_combinations, key=lambda x: x[7])
#     print(max_capacity_row)


#############################################################

# Checks using battery mass not pack mass



# # Rivian R1T
# req_capacity = 135000
# req_discharging_power = 511000
# req_max_V = 550
# req_min_V = 210
# req_max_mass_battery = 540
# req_charging_power = 210000

# Nissan Leaf
req_energy = 27700
req_discharging_power = 90000
req_max_V = 398
req_min_V = 240
req_max_mass_battery = 185.5
req_max_mass_pack = 315
req_charging_power = 50000



def Calculate_Possible_Combinations(req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_pack, req_charging_power, car_data, max_volume):
    
    import time
    start_time = time.time()


    print("Started")
    battery_data = {}

    battery_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="RAW DATA")

    i = 1
    battery_data = {f"battery_{i}_index": battery_database.iloc[i].tolist() for i in range(349)}  # Adjusted for 348 rows

    print("Battery Data Imported")

    batteries_to_be_removed = []
    print(req_energy/req_max_mass_pack)
 
 
    for i in range(1, 333):

        energy_density = (battery_data[f"battery_{i}_index"][14] * battery_data[f"battery_{i}_index"][16])/ (battery_data[f"battery_{i}_index"][21]/1000) # Energy density

        if energy_density < (req_energy/req_max_mass_pack)/1.2:
            batteries_to_be_removed.append(i)

    print(f"Batteries to be removed: {batteries_to_be_removed}")

    # for i in range(len(batteries_to_be_removed)):
    #     battery_data.pop(f"battery_{batteries_to_be_removed[i]}_index")

    WLTP_data = {}

    WLTP_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="WLTP Acc")
    i = 1 

    WLTP_data = {f"WLTP_{i}_index": WLTP_database.iloc[i].tolist() for i in range(1493)}  # Adjusted for 1211 rows
    # print(len(WLTP_data))
    # print(WLTP_data[f"WLTP_{1490}_index"][4], WLTP_data[f"WLTP_{1491}_index"][4], WLTP_data[f"WLTP_{1492}_index"][4])

    print("WLTP Data Imported")

    # successful_combinations, count_successful_combinations_2_bat, total_checked = Find_Two_Battery_Options(battery_data, req_energy, req_discharging_power, req_max_V, \
    #                                                                                 req_min_V, req_max_mass_pack, req_charging_power)
    end_time_2_bat = time.time()
    for successful_combinations, count_successful_combinations_2_bat, total_checked in Find_Two_Battery_Options_Test_with_removed(battery_data, req_energy, req_discharging_power, req_max_V, \
                                                                                    req_min_V, req_max_mass_pack, req_charging_power, batteries_to_be_removed, max_volume):
        yield successful_combinations, 0, count_successful_combinations_2_bat, 0, total_checked
        
    if successful_combinations == []:
        for successful_combinations, count_successful_combinations_2_bat, total_checked in Find_Two_Battery_Options_Test(battery_data, req_energy, req_discharging_power, req_max_V, \
                                                                                    req_min_V, req_max_mass_pack, req_charging_power, max_volume):
            yield successful_combinations, 0, count_successful_combinations_2_bat, 0, total_checked
        
    print(f"total checked: {total_checked}")
    end_time_2_bat_test = time.time()  # End timer

    successful_combinations_1_bat, count_successful_combinations_1_bat = Find_One_Battery_Options(battery_data, req_energy, req_discharging_power, req_max_V, \
                                                                                    req_min_V, req_max_mass_pack, req_charging_power, max_volume)


    for i in range(len(successful_combinations_1_bat)):
        successful_combinations.append(successful_combinations_1_bat[i])

    # successful_combinations_store = [battery_1_index(0), battery_1_series(1), battery_1_parallel(2),
                                    # battery_2_index(3), battery_2_series(4), battery_2_parallel(5),
                                    # capacity(6), discharging_power(7), mass(8), charging_power(9), range(10)
                                    # min_total_time(11), std_total_time(12), max_total_power(13)]

    end_time_after_finding_combinations = time.time()  # End timer

    elapsed_time_1_bat = end_time_after_finding_combinations - end_time_2_bat_test
    elapsed_time_test = end_time_2_bat_test - end_time_2_bat
    elapsed_time_2_bat = end_time_2_bat - start_time
    total_time = end_time_after_finding_combinations - start_time

    # print(f"Elapsed time 1 bat: {elapsed_time_1_bat:.6f} seconds")
    # print(f"Elapsed time 2 bat: {elapsed_time_2_bat:.6f} seconds")
    # print(f"Elapsed time 2 bat test: {elapsed_time_test:.6f} seconds")
    print(f"Total time: {total_time:.2f} seconds")
            
    print(f"2-Batteries count: {count_successful_combinations_2_bat}, 1-Battery count: {count_successful_combinations_1_bat}")

    if successful_combinations:
        max_energy_row = max(successful_combinations, key=lambda x: x[6])
        min_mass_row = min(successful_combinations, key=lambda x: x[8])
        # print(f"Min mass: {min_mass_row}")
        # print(f"Max energy: {max_energy_row}")

    # car_data = [3100, 0.3, 3.38, 0.015, 0] # Rivian R1T             Actual: 505, Calculated: 508
    # car_data = [1748, 0.29, 2.37, 0.015, 0] # Kia Niro EV         Actual: 384, Calculated: 405
    # car_data = [1486, 0.28, 2.33, 0.015, 0] # Nissan Leaf         Actual: 169(excel)/135, Calculated: 179 Using 2 chems: 310
    # car_data = [1830, 0.23, 2.268, 0.015, 0] # Tesla model 3      Actual: 576, Calculated: 572
    # car_data = [2584, 0.29, 2.3, 0.015, 0] # Polestar 3              Actual: 482, Calculated: 532

    start_time_range = time.time()
    

    if successful_combinations:
        for i in range(0, len(successful_combinations)):
            battery_data_series_parallel = [successful_combinations[i][1], successful_combinations[i][2], successful_combinations[i][4], successful_combinations[i][5]]
            battery_1 = battery_data[f"battery_{successful_combinations[i][0]}_index"]
            battery_2 = battery_data[f"battery_{successful_combinations[i][3]}_index"]

            # print(f"Battery number series parallel {successful_combinations[i][0], successful_combinations[i][1], successful_combinations[i][2], successful_combinations[i][3], successful_combinations[i][4], successful_combinations[i][5]}")

            Range = Range_Estimation_for_Batteries(WLTP_data, car_data, battery_data_series_parallel, battery_1, battery_2)

            successful_combinations[i].append(Range)

            # print(f"Range {i}: {Range} km")
    
    end_time_range = time.time()  # End timer

    elapsed_time = end_time_range - start_time_range
    print(f"Elapsed time for range estimation: {elapsed_time:.6f} seconds")

    if successful_combinations:
        max_range_row = max(successful_combinations, key=lambda x: x[10])
        min_range_row = min(successful_combinations, key=lambda x: x[10])
        max_capacity_row = max(successful_combinations, key=lambda x: x[6])
        min_mass_row = min(successful_combinations, key=lambda x: x[8])

        # print(f"Last row: {successful_combinations[-1:]}")

    # print(f"Min mass: {min_mass_row}")
    # print(f"Max capacity: {max_capacity_row}")
    # print(f"Max range: {max_range_row}")
    # print(f"Min range: {min_range_row}")
    atart_time_charging = time.time()
    if successful_combinations:
        for i in range(0, len(successful_combinations)):

            battery_data_series_parallel = [successful_combinations[i][1], successful_combinations[i][2], successful_combinations[i][4], successful_combinations[i][5]] # battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel
            battery_1 = battery_data[f"battery_{successful_combinations[i][0]}_index"]
            battery_2 = battery_data[f"battery_{successful_combinations[i][3]}_index"]
            
            min_total_time, std_total_time, max_total_power = Charging_times(battery_data_series_parallel, battery_1, battery_2)

            successful_combinations[i].append(min_total_time)
            successful_combinations[i].append(std_total_time)
            successful_combinations[i].append(max_total_power)

    end_time_charging = time.time()  # End timer

    elapsed_time = end_time_charging - atart_time_charging
    print(f"Elapsed time for charging times estimation: {elapsed_time:.6f} seconds")

    # print(successful_combinations[1])
    start_time_before_comparing = time.time()  # End timer

    
    if len(successful_combinations) > 0:
        best_weighted_normaliesed, max_range_row = Compare_Best_Combination(successful_combinations)
        # print(f"Best normalised weighted row: {best_weighted_normaliesed},\nMax range: {max_range_row}")
        # print(f"Max, Min charging time {max(successful_combinations, key=lambda x: x[11])}")
        # print(f"Min mass {min(successful_combinations, key=lambda x: x[8])}")
    else:
        best_weighted_normaliesed = 0
        max_range_row = 0

    end_time_after_comparing = time.time()
    elapsed_time_2 = end_time_after_comparing - start_time_before_comparing
    print(f"Elapsed time for comparison: {elapsed_time_2:.6f} seconds")

    # data = {successful_combinations[9], successful_combinations[11]}
    # df = pd.DataFrame(data)
    # df.to_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="Test", index=False)

    yield successful_combinations, best_weighted_normaliesed, count_successful_combinations_2_bat, count_successful_combinations_1_bat, total_checked
    
  # return best_weighted_normaliesed, 

#x = Calculate_Possible_Combinations(req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_pack, req_charging_power)

#############################################################


# single_bat_success = 0
# count_successful_batteries = 0
# successful_batteries = []

# # # # Rivian R1T
# # # req_capacity = 135000
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


# while single_bat_success == 0:

#     # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
#     multi_bat_success, battery_1_series, battery_1_parallel, capacity, discharging_power, mass, charging_power = \
#     One_Chem_Comparison(battery_data[f"battery_{battery_1_index}_index"], req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power)
#     # battery_1, req_capacity, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req

#     if single_bat_success == 1:
#         # print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")
        
#         successful_batteries.append([
#             battery_1_index, battery_1_series, battery_1_parallel,
#             capacity, discharging_power, mass, charging_power])
        
#         single_bat_success = 0
#         count_successful_batteries += 1

#     if battery_1_index == 333:
#         break
#     else:
#         battery_1_index += 1
    

#     # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
    
# print(count_successful_batteries)

# if successful_batteries:
#     max_capacity_row_single_bat = max(successful_batteries, key=lambda x: x[7])
#     print(max_capacity_row_single_bat)



#############################################################



# success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel = \
#     Two_Chemistries(battery_1_index, battery_2_index, 75000, 200000, 250, 475, 360, 318)
# # print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")

# while multi_bat_success== 0:
#     if battery_2_index == 388:
#         battery_1_index += 1
#         battery_2_index = battery_1_index
#     else:
#         battery_2_index += 1
    
#     success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel = \
#     Two_Chemistries(battery_1_index, battery_2_index, 75000, 200000, 250, 475, 360, 318)

#     print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
    
#     if multi_bat_success== 1:
#         print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")
#         break

# Two_Chemistries(required_cap, battery_1, battery_2, peak_power_required, min_pack_voltage, max_pack_voltage, pack_voltage, max_mass(kg))
# print(min_battery_1_only, min_battery_2_only)