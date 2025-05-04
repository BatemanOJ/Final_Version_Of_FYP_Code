# this version doesn't search through the excel on each run to find the row data 
# so chould be quicker

import math 
import numpy as np

# from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1
# from Get_Data_From_Cell import Get_Data_Battery_Cell # row -3, column -2
# from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array
from Find_Power_Dense_Battery import Find_Power_Dense_Battery_Efficient
from Check_Constraints import Check_Mass, Check_Max_V, Check_Min_V
from Calculate_Pack_Mass import Calculate_Mass_Two_Batteries



def Two_Chem_Efficient(battery_1, battery_2, req_capacity, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req):

    # Battery 1 is the energy dense one and battery 2 is the power dense one
    battery_1, battery_2, battery_1_Wh, battery_2_Wh = Find_Power_Dense_Battery_Efficient(battery_1, battery_2)

    min_battery_1_only = math.ceil(req_capacity/(battery_1_Wh))
    min_battery_2_only = math.ceil(req_capacity/(battery_2_Wh))

    no_battery_1 = math.ceil(min_battery_1_only/3)
    no_battery_2 = math.ceil(min_battery_2_only/3)

    capacity = no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh
    pack_mass = Calculate_Mass_Two_Batteries(battery_1, battery_2, no_battery_1, no_battery_2)
    # print(f"Pre-tests, Capacity: {capacity} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}")

    while req_capacity > capacity and pack_mass <= max_mass:

        if req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10

        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1
        
        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
            no_battery_2 += 100

        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
            no_battery_2 += 10
        
        else:
            no_battery_2 += 1
        
        capacity = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        pack_mass = Calculate_Mass_Two_Batteries(battery_1, battery_2, no_battery_1, no_battery_2)

        if pack_mass > max_mass:
            # print(f"Maximum mass exceeded: {pack_mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0, capacity, 0, pack_mass, 0
        # else:
            
    # print(f"Capacity: {capacity} Batteries: {no_battery_1, no_battery_2}, Mass: {pack_mass}")

    max_pack_V = battery_1[15] * no_battery_1 + battery_2[15] * no_battery_2

    counter_max_voltage = 0
    check_mass = 1 
    check_max_V = 0
    no_battery_1_parallel = 1
    no_battery_2_parallel = 1
    no_battery_1_series = no_battery_1
    no_battery_2_series = no_battery_2

    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)

    while check_max_V == 0 and check_mass == 1 and check_min_V == 1:

        if no_battery_2_series < no_battery_1_series:
            no_battery_1_series = no_battery_1_series - math.floor(no_battery_1_series/(1+no_battery_1_parallel))
            no_battery_1_parallel += 1
        else:
            no_battery_2_series = no_battery_2_series - math.floor(no_battery_2_series/(1+no_battery_2_parallel))
            no_battery_2_parallel += 1

        # if counter_max_voltage > 1000:
        #     success = 0
        #     return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, mass, 0
        # counter_max_voltage += 1

        check_mass, pack_mass = Check_Mass(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        counter = 0
        while check_mass == 0:
            # print(no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel)
            counter+=1
            # if counter > 100000:
            #     print("B")
            #     success = 2
            #     return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, pack_mass, 0
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
                # print(f"Exit: {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
                return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, pack_mass, 0
            
            check_mass, pack_mass = Check_Mass(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
            
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)

        if check_min_V == 0:
            success = 0
            # print(f"Exit V-min: {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, pack_mass, 0
    
    # print(f"Voltage Check Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}")

    battery_1_peak_power = battery_1[16] * battery_1[19]
    battery_2_peak_power = battery_2[16] * battery_2[19]

    peak_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_power 
    # print(f"Power: {peak_power_generated}, Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    while peak_power_req > peak_power_generated and check_mass == 1 and check_max_V == 1:
        
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

        check_mass, pack_mass = Check_Mass(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0:
            # print(f"Mass or voltage over limit{pack_mass, max_pack_V, min_pack_V}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, pack_mass, 0

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {pack_mass}")
    
    battery_1_peak_charge_power = battery_1[16] * battery_1[23]
    battery_2_peak_charge_power = battery_2[16] * battery_2[23]

    peak_charge_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_charge_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_charge_power
    
    # print(f"Discharging Power {peak_charge_power_req, peak_charge_power_generated}")

    while peak_charge_power_req > peak_charge_power_generated and check_mass == 1 and check_max_V == 1:
        
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

        # print(f"Charging Power 2{peak_charge_power_req, peak_charge_power_generated}")

        check_mass, pack_mass = Check_Mass(battery_1, battery_2, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0:
            # print(f"Mass or voltage over limit{mass, max_pack_V}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, 0, pack_mass, 0

        

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    # print(f"Charging Power {peak_charge_power_req, peak_charge_power_generated}")

    success = 1

    return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, capacity, peak_power_generated, pack_mass, peak_charge_power_generated