



def Meets_Conditions(successful_combination, average_range, average_mass, average_discharging_power, average_charging_power):
    counter = 0
    fail = 0
    if successful_combination[10] > average_range:
        counter += 1
    else:
        fail = 1
    
    if successful_combination[8] < average_mass:
        counter += 1
    else:
        fail = 2
    
    if successful_combination[7] > average_discharging_power:
        counter += 1
    else:
        fail = 3
    
    if successful_combination[9] > average_charging_power:
        counter += 1
    else:
        fail = 4
    
    conditions_met = [counter, fail]
    
    return conditions_met
