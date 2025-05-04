



def Calculate_Mass_Two_Batteries(Battery_1, Battery_2, no_battery_1, no_battery_2):
    if Battery_1[39] == 1:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/60.25) * 100
    
    elif Battery_1[39] == 2:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/60.79) * 100

    elif Battery_1[39] == 3:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/64.69) * 100


    if Battery_2[39] == 1:
        battery_2_pack_mass = ((no_battery_2 * (Battery_2[21]/1000))/60.25) * 100
    
    elif Battery_2[39] == 2:
        battery_2_pack_mass = ((no_battery_2 * (Battery_2[21]/1000))/60.79) * 100

    elif Battery_2[39] == 3:
        battery_2_pack_mass = ((no_battery_2 * (Battery_2[21]/1000))/64.69) * 100

    # print(Battery_1[21], Battery_2[21])
    # print(f"battery 1 and 2 mass {battery_1_pack_mass, battery_2_pack_mass}")

    total_mass = battery_1_pack_mass + battery_2_pack_mass
    return total_mass
    


def Calculate_Mass_One_Batteries(Battery_1, no_battery_1):

    # print(Battery_1)

    if Battery_1[39] == 1:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/60.25) * 100
    
    elif Battery_1[39] == 2:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/60.79) * 100

    elif Battery_1[39] == 3:
        battery_1_pack_mass = ((no_battery_1 * (Battery_1[21]/1000))/64.69) * 100

    return battery_1_pack_mass