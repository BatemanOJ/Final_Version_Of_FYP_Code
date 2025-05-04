


def Check_Battery_Order (battery_data, battery_1_index, battery_2_index, battery_1_series, battery_1_parallel, \
                         battery_2_series, battery_2_parallel, capacity):
    
    # battery_data[f"battery_{battery_1_index}_index"], battery_data[f"battery_{battery_2_index}_index"]

    capacity_no_switch = battery_data[f"battery_{battery_1_index}_index"][14] * battery_data[f"battery_{battery_1_index}_index"][16] * battery_1_series * battery_1_parallel\
        + battery_data[f"battery_{battery_2_index}_index"][14] * battery_data[f"battery_{battery_2_index}_index"][16] * battery_2_series * battery_2_parallel

    capacity_switch = battery_data[f"battery_{battery_1_index}_index"][14] * battery_data[f"battery_{battery_1_index}_index"][16] * battery_2_series * battery_2_parallel\
        + battery_data[f"battery_{battery_2_index}_index"][14] * battery_data[f"battery_{battery_2_index}_index"][16] * battery_1_series * battery_1_parallel
    
    # print(f"Capacity no switch: {capacity_no_switch}, Capacity switch: {capacity_switch}, Capacity: {capacity}")
    
    if capacity == capacity_no_switch:
        return 1
    elif capacity == capacity_switch:
        return 0
