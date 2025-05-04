import math 
import numpy as np

from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1
from Get_Data_From_Cell import Get_Data_Battery_Cell # row -3, column -2
from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array
from Find_Power_Dense_Battery import Find_Power_Dense_Battery
from Check_Constraints import Check_Mass, Check_Max_V


def Two_Chemistries(battery_1, battery_2, req_capacity, peak_power_req, min_pack_V_req, max_pack_V_allowed, pack_voltage, max_mass):


    # Battery 1 is the energy dense one and battery 2 is the power dense one
    battery_1, battery_2, battery_1_Wh, battery_2_Wh = Find_Power_Dense_Battery(battery_1, battery_2)

    min_battery_1_only = math.ceil(req_capacity/(battery_1_Wh))
    min_battery_2_only = math.ceil(req_capacity/(battery_2_Wh))

    no_battery_1 = math.ceil(min_battery_1_only/3)
    no_battery_2 = math.ceil(min_battery_2_only/3)

    capacity = no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh
    mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)
    # print(f"Capacity: {capacity} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    while req_capacity > capacity and mass <= max_mass:

        if req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10

        elif req_capacity - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1
        
        else:
            no_battery_2 += 1
        
        capacity = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)

        if mass > max_mass:
            # print(f"Maximum mass exceeded: {mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0
        else:
            print(f"Capacity: {capacity} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")
    

    max_pack_voltage = battery_1[15] * no_battery_1 + battery_2[15] * no_battery_2

    counter_max_voltage = 0
    check_mass = 1 
    check_max_V = 0
    no_battery_1_parallel = 1
    no_battery_2_parallel = 1
    no_battery_1_series = no_battery_1
    no_battery_2_series = no_battery_2

    while check_max_V == 0 and check_mass == 1:

        if no_battery_2_series < no_battery_1_series:
            no_battery_1_series = no_battery_1_series - math.floor(no_battery_1_series/(1+no_battery_1_parallel))
            no_battery_1_parallel += 1
        else:
            no_battery_2_series = no_battery_2_series - math.floor(no_battery_2_series/(1+no_battery_2_parallel))
            no_battery_2_parallel += 1

        if counter_max_voltage > 1000:
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel
        counter_max_voltage += 1

        check_mass, mass = Check_Mass(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        while check_mass == 0:
            if no_battery_1_parallel > no_battery_2_parallel:
                no_battery_2_series -= 1
            else:
                no_battery_1_series -= 1
            
            check_mass, mass = Check_Mass(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
            
            # print(f"Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}")


        check_max_V, max_pack_voltage = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)

        
        # print(f"Check mass: {check_mass}, Check voltage:{check_max_V}")
        print(f"Voltage: {max_pack_voltage, max_pack_V_allowed} Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}")

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

        elif req_capacity - peak_power_generated > (no_battery_2_parallel * battery_2_peak_power):
            no_battery_2_series += 1

        elif req_capacity - peak_power_generated > (no_battery_1_parallel * battery_1_peak_power):
            no_battery_1_series += 1
        
        else:
            if no_battery_2_parallel > no_battery_1_parallel:
                no_battery_1_series += 1
            else:
                no_battery_2_series += 1
        
        peak_power_generated = no_battery_1_series * no_battery_1_parallel * battery_1_peak_power + \
                           no_battery_2_series * no_battery_2_parallel * battery_2_peak_power 
        # mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)

        check_mass, mass = Check_Mass(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_voltage = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)

        if check_mass == 0 or check_max_V == 0:
            # print(f"Mass or voltage over limit{mass, max_pack_voltage}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel 

        print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")
    success = 1

    return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel