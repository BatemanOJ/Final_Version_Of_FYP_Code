# this version doesn't search through the excel on each run to find the row data 
# so should be quicker

import math 
import numpy as np
import pandas as pd

# from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1
# from Get_Data_From_Cell import Get_Data_Battery_Cell # row -3, column -2
# from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array
from Find_Power_Dense_Battery import Find_Power_Dense_Battery_Efficient
from Check_Constraints import Check_Mass_Battery_Only, Check_Max_V, Check_Min_V, Check_energy
from Pack_Volume_Calculator import volume_calculator
from check_power import check_power

battery_data = {}

battery_database = pd.read_excel("Battery database from open source_CellDatabase_v6.xlsx", sheet_name="RAW DATA")

i = 1
battery_data = {f"battery_{i}_index": battery_database.iloc[i].tolist() for i in range(348)}  # Adjusted for 348 rows

# print("Battery Data Imported")

def Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_1, battery_2, req_energy, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req, max_volume):

    original_max_mass = max_mass
    # Battery 1 is the energy dense one and battery 2 is the power dense one
    battery_1, battery_2, battery_1_Wh, battery_2_Wh = Find_Power_Dense_Battery_Efficient(battery_1, battery_2)

    min_battery_1_only = math.ceil(req_energy/(battery_1_Wh))
    min_battery_2_only = math.ceil(req_energy/(battery_2_Wh))

    no_battery_1 = math.ceil(min_battery_1_only/3)
    no_battery_2 = math.ceil(min_battery_2_only/3)

    energy = no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh
    pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
    # print(f"Total volume 1: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    if pack_mass > max_mass:
        while pack_mass > max_mass:
            if no_battery_1 > 1 and no_battery_1 >= no_battery_2:
                no_battery_1 -= 1

            elif no_battery_2 > 1 and no_battery_2 > no_battery_1:
                no_battery_2 -= 1

            else:
                success = 0
                # print(f"Fail. Mass over limit: {mass}")
                return success, no_battery_1, 0, no_battery_2, 0, energy, 0, pack_mass, 0, 0
            
            pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
            # print(f"Mass reducer, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")
    
    
    # print(f"Total volume 2: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")
    # if battery_1[27] == 275:
        # print(f"Pack mass: {pack_mass}, Maximum: {max_mass}")

    max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)

    # if battery_1[27] == 275:
    #     print(f"Maximum mass: {max_mass}")


    # check_which_battery = 1
    # while pack_mass <= max_mass and volume_check == 1:
    #     #while req_energy > energy and pack_mass <= max_mass and volume_check == 1:
        
    #     if req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
    #         no_battery_1 += 100

    #     elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
    #         no_battery_1 += 10

    #     elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
    #         no_battery_1 += 1
        
    #     elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
    #         no_battery_2 += 100

    #     elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
    #         no_battery_2 += 10
        
    #     elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) >= 0:
    #         no_battery_2 += 1

    #     energy = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
    #     pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
    #     total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
    #     max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    #     # print(f"Mass: {mass}, energy: {energy}")
    #     # print(f"pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")
    #     # print(f"pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    #     battery_masses = [battery_1[21], battery_2[21]]
        
    #     if 0 < max_mass - pack_mass and max_mass - pack_mass < max(battery_masses)/1000 and req_energy <= energy:
    #         # print(f"battery mass 1: {battery_masses[0]}, battery mass 2: {battery_masses[1]}")
    #         # print(f"left over: {max_mass - pack_mass}, {max(battery_masses)}")
    #         # print(f"In if  pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")
    #         break
    #     elif pack_mass > max_mass:
    #         # print(f"Maximum mass exceeded: {pack_mass}, Maximum: {max_mass}")
    #         success = 0
    #         return success, no_battery_1, 0, no_battery_2, 0, energy, 0, pack_mass, 0, 0

    #     if req_energy <= energy and check_which_battery == 1:
    #         no_battery_1 += 1
    #         check_which_battery = 0
    #     elif req_energy <= energy and check_which_battery == 0:
    #         no_battery_2 += 1
    #         check_which_battery = 1

    # print(f"pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    while req_energy > energy and pack_mass <= max_mass and volume_check == 1:
        
        mass_left = max_mass - pack_mass

        if req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10
        
        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
            no_battery_2 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
            no_battery_2 += 10
        
        else: 
            no_battery_2 += 1

        energy = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        # print(f"Mass: {mass}, energy: {energy}")
        
        if pack_mass> max_mass:
            # print(f"Maximum mass exceeded: {mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0, energy, 0, pack_mass, 0, 0

    mass_left = max_mass - pack_mass
    stored_req_energy = req_energy

    # print(f"After initial, pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    if mass_left > 0 and mass_left/max_mass > 0.75:
        req_energy = req_energy*1.75
        # print(f"75% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.65:
        req_energy = req_energy*1.65
        # print(f"65% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.55:
        req_energy = req_energy*1.55
        # print(f"55% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.45:
        req_energy = req_energy*1.45
        # print(f"45% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.35:
        req_energy = req_energy*1.35
        # print(f"35% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.25:
        # print(f"25% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.25
    elif mass_left > 0 and mass_left/max_mass > 0.15:
        # print(f"15% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.15
    elif mass_left > 0 and mass_left/max_mass > 0.05:
        # print(f"5% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.05

    # print(f"After req increase, pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    while req_energy > energy and pack_mass <= max_mass and volume_check == 1:
        
        # mass_left = max_mass - pack_mass

        if req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10
        
        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
            no_battery_2 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
            no_battery_2 += 10
        
        else: 
            no_battery_2 += 1

        energy = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        # print(f"Mass: {mass}, energy: {energy}")
        
        if pack_mass> max_mass:
            # print(f"Maximum mass exceeded: {mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0, energy, 0, pack_mass, 0, 0
        
    # print(f"After increase implmented, pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    mass_left = max_mass - pack_mass

    if mass_left > 0 and mass_left/max_mass > 0.75:
        req_energy = req_energy*1.75
        # print(f"75% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.65:
        req_energy = req_energy*1.65
        # print(f"65% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.55:
        req_energy = req_energy*1.55
        # print(f"55% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.45:
        req_energy = req_energy*1.45
        # print(f"45% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.35:
        req_energy = req_energy*1.35
        # print(f"35% Mass left: {mass_left}, max_mass: {max_mass}")
    elif mass_left > 0 and mass_left/max_mass > 0.25:
        # print(f"25% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.25
    elif mass_left > 0 and mass_left/max_mass > 0.15:
        # print(f"15% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.15
    elif mass_left > 0 and mass_left/max_mass > 0.05:
        # print(f"5% Mass left: {mass_left}, max_mass: {max_mass}")
        req_energy = req_energy*1.05

    # print(f"2 After req increase, pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")

    while req_energy > energy and pack_mass <= max_mass and volume_check == 1:
        
        # mass_left = max_mass - pack_mass

        if req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10
        
        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
            no_battery_2 += 100

        elif req_energy - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
            no_battery_2 += 10
        
        else: 
            no_battery_2 += 1

        energy = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        pack_mass = (((no_battery_1 * (battery_1[21]/1000))/battery_1[40]) * 100) + (((no_battery_2 * (battery_2[21]/1000))/battery_2[40]) * 100)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        # print(f"Mass: {mass}, energy: {energy}")
        
        if pack_mass> max_mass:
            # print(f"Maximum mass exceeded: {mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0, energy, 0, pack_mass, 0, 0
        
    # req_energy = stored_req_energy
        
    # print(f"2 After increase implmented, pack_mass: {pack_mass}, max_mass: {max_mass}, volume_check: {volume_check}, Energy: {energy}, req_energy: {req_energy}")
    
    mass_left = max_mass - pack_mass
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1, 1, no_battery_2, 1, max_volume)
    # print(f"Total volume 3: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    max_pack_V = battery_1[15] * no_battery_1 + battery_2[15] * no_battery_2


    dont_reduce_series = 1
    check_reduce_series = 0
    

    no_battery_1_parallel = 1
    no_battery_2_parallel = 1
    no_battery_1_series = no_battery_1
    no_battery_2_series = no_battery_2

    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
    check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
    check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

    # print(f"First energy check{check_energy, energy}")
    while check_max_V == 0:# and check_mass == 1 and check_min_V == 1 and check_energy == 1:

        if check_energy == 1 and check_max_V == 0 and check_min_V == 1 and check_mass == 1 and dont_reduce_series == 1 and volume_check == 1:
            stored_no_battery_1_series = no_battery_1_series
            stored_no_battery_2_series = no_battery_2_series
            while check_energy == 1 and check_max_V == 0 and check_min_V == 1 and check_mass == 1:
                if battery_1[15] > battery_2[15] and battery_1_Wh < battery_2_Wh and (max_pack_V - max_pack_V_allowed) > (battery_1[15]*10):
                    no_battery_1_series -= 10

                elif battery_1[15] < battery_2[15] and battery_1_Wh > battery_2_Wh and (max_pack_V - max_pack_V_allowed) > (battery_2[15]*10):
                    no_battery_2_series -= 10 
                
                elif battery_1[15] > battery_2[15] and battery_1_Wh < battery_2_Wh:
                    no_battery_1_series -= 1

                elif battery_1[15] < battery_2[15] and battery_1_Wh > battery_2_Wh:
                    no_battery_2_series -= 1

                elif check_reduce_series == 0:
                    no_battery_1_series -= 1
                    check_reduce_series = 1
                
                elif check_reduce_series == 1:
                    no_battery_2_series -= 1
                    check_reduce_series = 0

                check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
                check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
                check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
                max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
                total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)
                # print(f"Reduce series Check: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, energy: {energy, req_energy}")

            if check_energy == 1 and check_max_V == 1 and check_min_V == 1 and check_mass == 1 and volume_check == 1:
                # print("Success")
                break
            else: 
                no_battery_1_series = stored_no_battery_1_series
                no_battery_2_series = stored_no_battery_2_series
                dont_reduce_series = 0
                # print(f"dont_reduce_series: {dont_reduce_series}")

        
        if no_battery_2_series < no_battery_1_series:
            no_battery_1_series = no_battery_1_series - math.floor(no_battery_1_series/(1+no_battery_1_parallel))
            no_battery_1_parallel += 1
        else:
            no_battery_2_series = no_battery_2_series - math.floor(no_battery_2_series/(1+no_battery_2_parallel))
            no_battery_2_parallel += 1

        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        while check_mass == 0:
            if no_battery_1_parallel > no_battery_2_parallel and \
                no_battery_1_parallel > 0 and no_battery_2_parallel > 0 and \
                no_battery_1_series > 0 and no_battery_2_series > 1:

                no_battery_2_series -= 1

            elif no_battery_1_parallel < no_battery_2_parallel and \
                no_battery_1_parallel > 0 and no_battery_2_parallel > 0 and \
                no_battery_1_series > 1 and no_battery_2_series > 0:

                no_battery_1_series -= 1
            
            else: 
                success = 0
                # print(f"Fail. pack_mass, voltage or energy over limit{pack_mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
                return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, pack_mass, 0, 0
            
            max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
            check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
            
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

        # print(f"Mass: {pack_mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")

        if check_min_V == 0 or check_energy == 0 or check_mass == 0 or volume_check == 0:
            # print(f"Fail. Mass, voltage or energy over limit{pack_mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, pack_mass, 0, 0
    
    # print(f"Voltage Check Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}")
    max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)
    # print(f"Total volume 4: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    battery_1_peak_power = battery_1[16] * battery_1[19]
    battery_2_peak_power = battery_2[16] * battery_2[19]

    peak_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_power 
    # print(f"Power: {peak_power_generated}, Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    while peak_power_req > peak_power_generated:# and check_mass == 1 and check_max_V == 1:
        
        if peak_power_req - peak_power_generated > (no_battery_2_series * battery_2_peak_power):
            no_battery_2_parallel += 1
        
        elif peak_power_req - peak_power_generated > (no_battery_1_series * battery_1_peak_power):
            no_battery_1_parallel += 1

        elif peak_power_req - peak_power_generated > (no_battery_2_parallel * battery_2_peak_power):
            no_battery_2_series += 1

        elif peak_power_req - peak_power_generated > (no_battery_1_parallel * battery_1_peak_power):
            no_battery_1_series += 1
        
        else:
            if no_battery_2_parallel > no_battery_1_parallel:
                no_battery_1_series += 1
            else:
                no_battery_2_series += 1
        
        peak_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_power 
        # mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)

        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)
        # print(f"Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}, Peak Power: {peak_power_req, peak_power_generated}")

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0 or volume_check == 0:
            # print(f"Fail. Mass, voltage or energy over limit{mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, pack_mass, 0, 0

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    # print(f"Discharging Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")
    
    battery_1_peak_charge_power = battery_1[16] * battery_1[23]
    battery_2_peak_charge_power = battery_2[16] * battery_2[23]
    max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)
    # print(f"Total volume 5: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    peak_charge_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_charge_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_charge_power
    
    # print(f"Charging Power 1{peak_charge_power_req, peak_charge_power_generated}")

    while peak_charge_power_req > peak_charge_power_generated:# and check_mass == 1 and check_max_V == 1:
        
        if peak_charge_power_req - peak_charge_power_generated > (no_battery_2_series * battery_2_peak_charge_power):
            no_battery_2_parallel += 1
        
        elif peak_charge_power_req - peak_charge_power_generated > (no_battery_1_series * battery_1_peak_charge_power):
            no_battery_1_parallel += 1

        elif peak_charge_power_req - peak_charge_power_generated > (no_battery_2_parallel * battery_2_peak_charge_power):
            no_battery_2_series += 1

        elif peak_charge_power_req - peak_charge_power_generated > (no_battery_1_parallel * battery_1_peak_charge_power):
            no_battery_1_series += 1
        
        else:
            if no_battery_2_parallel > no_battery_1_parallel:
                no_battery_1_series += 1
            else:
                no_battery_2_series += 1
        
        peak_charge_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_charge_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_charge_power 
        # mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)

        # print(f"Mass: {max_mass, mass}, max-V: {max_pack_V_allowed, max_pack_V}, min-V: {min_pack_V_allowed, min_pack_V}, energy: {energy}, Check Cap: {check_energy}, \
            #   Peak Power: {peak_power_req, peak_power_generated} Peak Charge Power: {peak_charge_power_req, peak_charge_power_generated}")
        
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0 or volume_check == 0:
            # print(f"Fail. Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")            
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, pack_mass, 0, 0

        

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
    check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

    # print(f"Total volume 6: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0 or volume_check == 0:
        # print(f"Fail. Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")            
        success = 0
        return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, pack_mass, 0, 0
    
    # print(f"Charging Power 3{peak_charge_power_req, peak_charge_power_generated}")

    # Function to check if another battery can be added
    def can_add_battery(max_volume):
        max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
        check_mass, _ = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, _ = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, _ = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, _ = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
        total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

        # print(f"max mass: {max_mass}")
        # print(f"Checks: {check_mass, check_max_V, check_min_V, check_energy, volume_check}")

        return check_mass and check_max_V and check_min_V and check_energy and volume_check  # Returns True if all checks pass
    
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}, battery 1 mass: {battery_1[21]}, battery 2 mass: {battery_2[21]}")

    # **Add Batteries to Series**
    while True:
        no_battery_1_series += 1
        # print(f"1 series add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        # tests += 1
        if not can_add_battery(max_volume):
            no_battery_1_series -= 1
            # print(f"1 series sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            # fails += 1
            break  # Stop adding when constraint is exceeded

    while True:
        no_battery_2_series += 1
        # print(f"2 series add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        # tests += 1
        if not can_add_battery(max_volume):
            no_battery_2_series -= 1
            # print(f"2 series sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            # fails += 1
            break  # Stop adding when constraint is exceeded

    # **Add Batteries to Parallel**
    while True:
        no_battery_1_parallel += 1
        # print(f"1 parallel add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        # tests += 1
        if not can_add_battery(max_volume):
            no_battery_1_parallel -= 1
            # print(f"1 parallel sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            # fails += 1
            break  # Stop adding when constraint is exceeded

    while True:
        no_battery_2_parallel += 1
        # print(f"2 parallel add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        # tests += 1
        if not can_add_battery(max_volume):
            no_battery_2_parallel -= 1
            # print(f"2 parallel sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            # fails += 1
            break  # Stop adding when constraint is exceeded

    # print(f"Pre-tests 2, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}, Volume: {max_volume}")

    max_mass, max_volume = check_power(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, original_max_mass, max_volume, peak_power_req, peak_charge_power_req)
    check_mass, pack_mass = Check_Mass_Battery_Only(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
    check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_energy)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)

        
    success = 1
    # print(success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, peak_power_generated, mass, peak_charge_power_generated)
    total_volume, volume_check = volume_calculator(battery_1, battery_2, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, max_volume)
    # print(f"Total volume 7: {total_volume}")
    # print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {pack_mass}, Volume: {max_volume}")

    return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, peak_power_generated, pack_mass, peak_charge_power_generated, total_volume

battery_1 = 1
battery_2 = 2
req_energy = 28000
peak_power_req = 90000
max_pack_V_allowed = 400
min_pack_V_allowed = 240
max_mass = 315
peak_charge_power_req = 50000
max_volume = 0.485
# Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_data[f"battery_{battery_1}_index"], battery_data[f"battery_{battery_2}_index"], req_energy, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req, max_volume)


# battery_data[f"battery_{battery_1}_index"], battery_data[f"battery_{battery_2}_index"]