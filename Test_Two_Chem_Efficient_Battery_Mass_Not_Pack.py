# this version doesn't search through the excel on each run to find the row data 
# so should be quicker

import math 
import numpy as np

# from Get_Data_From_Cell import Get_Data_EVs # row -2, colum -1
# from Get_Data_From_Cell import Get_Data_Battery_Cell # row -3, column -2
# from Get_Data_From_Cell import Get_Battery_Data_Row # gets the row of data and puts it into an array
from Find_Power_Dense_Battery import Find_Power_Dense_Battery_Efficient
from Check_Constraints import Check_Mass_Battery_Only, Check_Max_V, Check_Min_V, Check_energy



def Two_Chem_Efficient_Battery_Mass_Not_Pack(battery_1, battery_2, req_cap, peak_power_req, max_pack_V_allowed, min_pack_V_allowed, max_mass, peak_charge_power_req, tests, fails):

    # Battery 1 is the energy dense one and battery 2 is the power dense one
    battery_1, battery_2, battery_1_Wh, battery_2_Wh = Find_Power_Dense_Battery_Efficient(battery_1, battery_2)

    min_battery_1_only = math.ceil(req_cap/(battery_1_Wh))
    min_battery_2_only = math.ceil(req_cap/(battery_2_Wh))

    no_battery_1 = math.ceil(min_battery_1_only/3)
    no_battery_2 = math.ceil(min_battery_2_only/3)

    energy = no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh
    mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)
    print(f"Pre-tests, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    if mass > max_mass:
        while mass > max_mass:
            if no_battery_1 > 1 and no_battery_1 >= no_battery_2:
                no_battery_1 -= 1

            elif no_battery_2 > 1 and no_battery_2 > no_battery_1:
                no_battery_2 -= 1

            else:
                success = 0
                print(f"Fail. Mass over limit: {mass}")
                return success, no_battery_1, 0, no_battery_2, 0, energy, 0, mass, 0, 0, 0
            
            mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)
            print(f"Mass reducer, energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    while req_cap > energy and mass <= max_mass:

        if req_cap - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_1_Wh:
            no_battery_1 += 100

        elif req_cap - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_1_Wh:
            no_battery_1 += 10

        elif req_cap - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > battery_1_Wh:
            no_battery_1 += 1
        
        elif req_cap - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 100 * battery_2_Wh:
            no_battery_2 += 100

        elif req_cap - (no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh) > 10 * battery_2_Wh:
            no_battery_2 += 10
        
        else:
            no_battery_2 += 1

        energy = math.floor(no_battery_1 * battery_1_Wh + no_battery_2 * battery_2_Wh)
        mass = no_battery_1 * (battery_1[21]/1000) + no_battery_2 * (battery_2[21]/1000)

        print(f"Mass: {mass}, energy: {energy}")

        if mass > max_mass:
            print(f"Maximum mass exceeded: {mass}, Maximum: {max_mass}")
            success = 0
            return success, no_battery_1, 0, no_battery_2, 0, energy, 0, mass, 0, 0, 0
        # else:
            
    print(f"energy: {energy} Batteries: {no_battery_1, no_battery_2}, Mass: {mass}")

    max_pack_V = battery_1[15] * no_battery_1 + battery_2[15] * no_battery_2

    # counter_max_voltage = 0
    # check_mass = 1 
    # check_max_V = 0
    
    dont_reduce_series = 1
    check_reduce_series = 0
    counter_check_reduces_series = 0
    counter_check_reduces_series_fail = 0

    no_battery_1_parallel = 1
    no_battery_2_parallel = 1
    no_battery_1_series = no_battery_1
    no_battery_2_series = no_battery_2

    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
    check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
    check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

    print(f"First energy check{check_energy, energy}")
    while check_max_V == 0:# and check_mass == 1 and check_min_V == 1 and check_energy == 1:

        

        if check_energy == 1 and check_max_V == 0 and check_min_V == 1 and check_mass == 1 and dont_reduce_series == 1:
            stored_no_battery_1_series = no_battery_1_series
            stored_no_battery_2_series = no_battery_2_series
            counter_check_reduces_series += 1
            while check_energy == 1 and check_max_V == 0 and check_min_V == 1 and check_mass == 1:
                if battery_1[15] > battery_2[15] and battery_1_Wh < battery_2_Wh:
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
                check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

                print(f"Reduce series Check: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, energy: {energy, req_cap}")

            if check_energy == 1 and check_max_V == 1 and check_min_V == 1 and check_mass == 1:
                print("Success")
                break
            else: 
                no_battery_1_series = stored_no_battery_1_series
                no_battery_2_series = stored_no_battery_2_series
                dont_reduce_series = 0
                counter_check_reduces_series_fail += 1
                print(f"dont_reduce_series: {dont_reduce_series}")

        print(f"{counter_check_reduces_series} Fail: {counter_check_reduces_series_fail}")

        if no_battery_2_series < no_battery_1_series:
            no_battery_1_series = no_battery_1_series - math.floor(no_battery_1_series/(1+no_battery_1_parallel))
            no_battery_1_parallel += 1
        else:
            no_battery_2_series = no_battery_2_series - math.floor(no_battery_2_series/(1+no_battery_2_parallel))
            no_battery_2_parallel += 1


        check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
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
                print(f"Fail. Mass, voltage or energy over limit{mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
                return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, mass, 0, 0, 0
            
            check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
            
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)
        check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)

        print(f"Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")

        if check_min_V == 0 or check_energy == 0 or check_mass == 0:
            print(f"Fail. Mass, voltage or energy over limit{mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, mass, 0, 0, 0
    
    print(f"Voltage Check Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}")

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

        check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

        print(f"Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}, Peak Power: {peak_power_req, peak_power_generated}")

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0:
            print(f"Fail. Mass, voltage or energy over limit{mass, max_pack_V, min_pack_V, energy}, Check Cap: {check_energy}")
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, mass, 0, 0, 0

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    print(f"Discharging Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")
    
    battery_1_peak_charge_power = battery_1[16] * battery_1[23]
    battery_2_peak_charge_power = battery_2[16] * battery_2[23]

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
        #       Peak Power: {peak_power_req, peak_power_generated} Peak Charge Power: {peak_charge_power_req, peak_charge_power_generated}")

        check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

        if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0:
            print(f"Fail. Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")            
            success = 0
            return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, mass, 0, 0, 0

        

        # print(f"Power: {peak_power_req, peak_power_generated}, Batteries: {no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel}, Mass: {mass}")

    check_mass, mass = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
    check_max_V, max_pack_V = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
    check_min_V, min_pack_V = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
    check_energy, energy = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

    if check_mass == 0 or check_max_V == 0 or check_min_V == 0 or check_energy == 0:
        print(f"Fail. Mass: {mass}, max-V: {max_pack_V}, min-V: {min_pack_V}, energy: {energy}, Check Cap: {check_energy}")            
        success = 0
        return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, 0, mass, 0, 0, 0
    
    print(f"Charging Power 3{peak_charge_power_req, peak_charge_power_generated}")

    
    # Function to check if another battery can be added
    def can_add_battery():
        check_mass, _ = Check_Mass_Battery_Only(battery_1[21], battery_2[21], no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, max_mass)
        check_max_V, _ = Check_Max_V(battery_1[15], battery_2[15], no_battery_1_series, no_battery_2_series, max_pack_V_allowed)
        check_min_V, _ = Check_Min_V(battery_1[17], battery_2[17], no_battery_1_series, no_battery_2_series, min_pack_V_allowed)
        check_energy, _ = Check_energy(battery_1_Wh, battery_2_Wh, no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel, req_cap)

        print(f"Checks: {check_mass, check_max_V, check_min_V, check_energy}")

        return check_mass and check_max_V and check_min_V and check_energy  # Returns True if all checks pass

    # **Add Batteries to Series**
    while True:
        no_battery_1_series += 1
        print(f"1 series add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        tests += 1
        if not can_add_battery():
            no_battery_1_series -= 1
            print(f"1 series sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            fails += 1
            break  # Stop adding when constraint is exceeded

    while True:
        no_battery_2_series += 1
        print(f"2 series add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        tests += 1
        if not can_add_battery():
            no_battery_2_series -= 1
            print(f"2 series sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            fails += 1
            break  # Stop adding when constraint is exceeded

    # **Add Batteries to Parallel**
    while True:
        no_battery_1_parallel += 1
        print(f"1 parallel add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        tests += 1
        if not can_add_battery():
            no_battery_1_parallel -= 1
            print(f"1 parallel sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            fails += 1
            break  # Stop adding when constraint is exceeded

    while True:
        no_battery_2_parallel += 1
        print(f"2 parallel add {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
        tests += 1
        if not can_add_battery():
            no_battery_2_parallel -= 1
            print(f"2 parallel sub {no_battery_1_series, no_battery_2_series, no_battery_1_parallel, no_battery_2_parallel}")
            fails += 1
            break  # Stop adding when constraint is exceeded

    success = 1

    return success, no_battery_1_series, no_battery_1_parallel, no_battery_2_series, no_battery_2_parallel, energy, peak_power_generated, mass, peak_charge_power_generated, tests, fails