


def Set_Default_Values_For_GUI(req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_pack, req_charging_power):

    if not req_energy:
        req_energy = 27700
    
    if not req_discharging_power:
        req_discharging_power = 90000

    if not req_max_V:
        req_max_V = 398

    if not req_min_V:
        req_min_V = 240

    if not req_max_mass_pack:
        req_max_mass_pack = 315

    if not req_charging_power:
        req_charging_power = 50000

def Values_From_Boxes(range, energy, discharging_power, max_V, min_V, max_mass_pack, charging_power, \
                      req_range, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_pack, req_charging_power):

    if range:
        req_range = range
    else:
        req_range = req_range

    if req_energy:
        req_energy = energy
    else:
        req_energy = req_energy
    
    if req_discharging_power:
        req_discharging_power = discharging_power
    else: 
        req_discharging_power = req_discharging_power

    if req_max_V:
        req_max_V = max_V
    else: 
        req_max_V = req_max_V

    if req_min_V:
        req_min_V = min_V
    else: 
        req_min_V = req_min_V

    if req_max_mass_pack:
        req_max_mass_pack = max_mass_pack
    else: 
        req_max_mass_pack = req_max_mass_pack

    if req_charging_power:
        req_charging_power = charging_power
    else: 
        req_charging_power = req_charging_power


    return req_range, req_energy, req_discharging_power, req_max_V, req_min_V, req_max_mass_pack, req_charging_power