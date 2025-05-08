
from One_Chem_Comparison import One_Chem_Comparison
from One_Chem_Comparison_27_04_fix import One_Chem_Comparison_27_04_Fix


def Find_One_Battery_Options(battery_data, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume):
    
    successful_batteries = []
    single_bat_success = 0
    count_successful_batteries = 0
    battery_1_index = 1


    while single_bat_success == 0:

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
        # single_bat_success, battery_1_series, battery_1_parallel, energy, discharging_power, mass, charging_power = \
        # One_Chem_Comparison(battery_data[f"battery_{battery_1_index}_index"], req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume)
        # battery_1, req_capacity, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
        single_bat_success, battery_1_series, battery_1_parallel, energy, discharging_power, mass, charging_power = \
        One_Chem_Comparison_27_04_Fix(battery_data[f"battery_{battery_1_index}_index"], req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume)
        

        if single_bat_success == 1:
            # print(f"Battery 1 Index: {battery_1_index} {battery_1_series}S {battery_1_parallel}P, Battery 2 Index: {battery_2_index} {battery_2_series}S {battery_2_parallel}P")
            
            successful_batteries.append([
                battery_1_index, battery_1_series, battery_1_parallel, 0, 0, 0,
                energy, discharging_power, mass, charging_power])
            
            single_bat_success = 0
            count_successful_batteries += 1

        if battery_1_index == 333:
            break
        else:
            battery_1_index += 1



    return successful_batteries, count_successful_batteries


from Two_Chem_Efficient_Battery_Mass_Not_Pack import Two_Chem_Efficient_Battery_Mass_Not_Pack
from Check_battery_index_order import Check_Battery_Order

def Find_Two_Battery_Options(battery_data, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume):
    
    battery_1_index = 1
    battery_2_index = 2

    multi_bat_success = 0
    count_successful_combinations = 0
    total_checked = 0
    successful_combinations = []

    while multi_bat_success == 0:

        Check_battery_1_order = battery_data[f"battery_{battery_1_index}_index"][1] 

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
        multi_bat_success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, energy, discharging_power, mass, charging_power = \
        Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"],\
                                                req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power)
        

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

        total_checked += 1

        if battery_1_index == 332 and battery_2_index == 333:
            break
        elif battery_2_index == 333:
            battery_1_index += 1
            battery_2_index = battery_1_index + 1
        else:
            battery_2_index += 1
     

    return successful_combinations, count_successful_combinations, total_checked



def Find_Two_Battery_Options_Test(battery_data, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume):
    
    battery_1_index = 1
    battery_2_index = 2

    multi_bat_success = 0
    count_successful_combinations = 0
    total_checked = 0
    successful_combinations = []

    while multi_bat_success == 0:

        Check_battery_1_order = battery_data[f"battery_{battery_1_index}_index"][1] 

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")
        multi_bat_success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, energy, discharging_power, mass, charging_power, battery_volume = \
        Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"],\
                                                req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume)
        

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

        total_checked += 1
        yield successful_combinations, count_successful_combinations, total_checked

        if battery_1_index == 332 and battery_2_index == 333:
            break
        elif battery_2_index == 333:
            battery_1_index += 1
            battery_2_index = battery_1_index + 1
        else:
            battery_2_index += 1
     

    return successful_combinations, count_successful_combinations, total_checked



def Find_Two_Battery_Options_Test_with_removed(battery_data, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power,\
                                               batteries_to_be_removed, max_volume):
    
    battery_1_index = 1
    battery_2_index = 2

    multi_bat_success = 0
    count_successful_combinations = 0
    total_checked = 0
    successful_combinations = []

    while multi_bat_success == 0:

        Check_battery_1_order = battery_data[f"battery_{battery_1_index}_index"][1] 

        # print(f"Battery 1 Index: {battery_1_index} Battery 2 Index: {battery_2_index}")

        multi_bat_success, battery_1_series, battery_1_parallel, battery_2_series, battery_2_parallel, energy, discharging_power, mass, charging_power, battery_volume = \
        Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"],\
                                                req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_battery, req_charging_power, max_volume)
        

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

        total_checked += 1
        yield successful_combinations, count_successful_combinations, total_checked

        if battery_1_index == 332 and battery_2_index == 333:
            break
        elif battery_2_index == 333:
            battery_1_index += 1
            if battery_1_index in batteries_to_be_removed:
                battery_1_index += 1
            battery_2_index = battery_1_index + 1
        else:
            battery_2_index += 1
            if battery_2_index in batteries_to_be_removed:
                battery_2_index += 1
     

    return successful_combinations, count_successful_combinations, total_checked